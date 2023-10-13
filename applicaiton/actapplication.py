import datetime
from datetime import date
import pandas as pd

from tool.excel_utils import compare, write_xlsx_sheets
from tool.json_utils import read_josn
from tool.mysql import mysql_init, select
from tool.sqlserver_pyodbc import sqlserver_init, read_sql
from tool.logging_utils import log_init


def compare_sql_list(log, mysql_con, sqlserver_con, sqlList):
    job_list = []
    execute_time_list = []
    source_list = []
    interfaceList = []
    endList = []
    execute_result_list = []
    remark_list = []
    for item in sqlList:
        try:
            mysqlResult = select(log, mysql_con, item['mysqlCenter'])
            sqlServerResult = read_sql(log, sqlserver_con, item['sqlServerSql'])
            job_list.append(item['name'])
            execute_time_list.append(datetime.datetime.now())
            source_list.append(item['sqlServerSql'])
            interfaceList.append(item['mysqlInterface'])
            endList.append(item['mysqlCenter'])

            compareFlag = len(mysqlResult) == len(sqlServerResult)
            execute_result_list.append(compareFlag)
            if compareFlag == False:
                remark_list.append('同步条数：SBI ' + str(len(sqlServerResult)) + ' & 中台 ' + str(len(mysqlResult)) + '条')
            else:
                remark_list.append('同步条数：' + str(len(sqlServerResult)) + '条')
            mysqlResultKey = pd.DataFrame()
            sqlServerResultKey = pd.DataFrame()
            for index, column in enumerate(item['mysqlField']):
                mysqlResultKey[item['mysqlField'][index]] = mysqlResult[item['mysqlField'][index]]
                sqlServerResultKey[item['mysqlField'][index]] = sqlServerResult[item['sqlServerField'][index]]
            # 空值填充
            mysqlResult.fillna(1)
            sqlServerResult.fillna(1)
            # 比对具体数据
            compare(log, mysqlResultKey, sqlServerResultKey, item['mysqlField'], item['name'])

        except Exception as e:
            log.error('%s compare Error %s', item['name'], e)

    data = {
        'job名称': job_list,
        '执行时间': execute_time_list,
        '源表sql': source_list,
        '中间表sql': interfaceList,
        '目标表sql': endList,
        '执行结果': execute_result_list,
        '备注': remark_list,
    }

    return pd.DataFrame(data)


def main_init(log):
    db_config = read_josn('db.json')
    mysql_config = db_config['mysql']
    sqlserver_config = db_config['sqlServer']
    mysql_con = mysql_init(mysql_config['host'], mysql_config['user'],
                           mysql_config['passwd'], mysql_config['db'])
    sqlserver_con = sqlserver_init(log, sqlserver_config['server'])
    compare_json_file = db_config['jsonFile']

    for file in compare_json_file:
        try:
            compare_json = read_josn(file)
            sheet_name = compare_json['name']
            file_name = str(date.today()) + '比对结果' + '.xlsx'

            compareSql = compare_json['sql']
            data = compare_sql_list(log, mysql_con, sqlserver_con, compareSql)
            write_xlsx_sheets(log, data, file_name, sheet_name)
        except Exception as e:
            log.error('Error %s jsonFile %s', e, file)


log = log_init()
try:
    main_init(log)
except Exception as e:
    log.error(e)
