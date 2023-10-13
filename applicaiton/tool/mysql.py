import pymysql
import pandas as pd


def mysql_init(host, user, password, database):
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    return conn.cursor()


def select(log, cursor, sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[column[0] for column in cursor.description])
