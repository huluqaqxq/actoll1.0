import pymssql
import uuid
import pandas as pd


# When I first started using this connection to sqlserver,
# I encountered many problems, so I enabled it.

# server    数据库服务器名称或IP
# user      用户名
# password  密码
# database  数据库名称


def sqlserver_init(server, user, password, database, type):
    server = server.replace(' ', '\\')
    if type == 'Windows':
        conn = pymssql.connect(server=server, database=database)
        return conn.cursor()
    else:
        conn = pymssql.connect(server=server, user=user, password=password, database=database)
        return conn.cursor()


def select(cursor, sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[column[0] for column in cursor.description])
