import pyodbc
import pandas as pd
import numpy as np


def sqlserver_init(log, server):
    log.info('当前驱动版本：' + str(pyodbc.drivers()))
    log.info('连接地址：' + str(server))
    return pyodbc.connect((server)).cursor()


def read_sql(log, cursor, sql):
    cursor.execute(sql)
    row = np.array(cursor.fetchall())
    log.info(f'Rows: {row[0]}, Columns: {[column[0] for column in cursor.description]}')
    result = pd.DataFrame(row, columns=[column[0] for column in cursor.description])
    return result
