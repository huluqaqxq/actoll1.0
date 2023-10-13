import pandas as pd
from datetime import date
import os
import xlsxwriter
import openpyxl


def mkdir(log, path):
    """ create directory if not exists
    :param log:
    :param path:
    :return:
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        log.info('---  This folder Create success %s!  ---', path)
    else:
        log.info('---  This folder exists %s!  ---', path)


def mkdir_xlsx(log, file_name):
    if os.path.exists(file_name):
        log.info('---  This fileName exists %s!  ---', file_name)
    else:
        workbook = xlsxwriter.Workbook(file_name)
        workbook.close()
        log.info('---  This fileName Create success %s!  ---', file_name)


def export_sheet(log, data, file_name):
    """ Use pandas to export excel without using index columns
    :param log:
    :param data:
    :param file_name:
    :return:
    """
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    log.info('fileName: %s to_excel success', file_name)


def write_xlsx_sheets(log, df, file_name, sheet_name):
    """ Use the openpyxl module to write a new sheet to an existing excel file
    :param log:
    :param df:
    :param file_name:
    :param sheet_name:
    :return:
    """
    mkdir_xlsx(log, file_name)
    with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
        workbook = writer.book
        # 删除指定sheet
        workbook.remove(workbook[sheet_name])
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()
    log.info("write_xlsx_sheets: %s %s success", file_name, sheet_name)


def compare(log, df1, df2, key, name):
    """ Use pandas merge method to merge primary keys
        Export differential data
    :param log:
    :param df1:
    :param df2:
    :param key:
    :param name:
    :return:

    """

    df1['SBI'] = '1'
    df2['interface'] = '2'
    log.info('-------------------------')
    log.info('df1 %s', df1)
    log.info('df2 %s', df2)
    merge_frame = pd.merge(df1, df2, on=key, how='outer')
    log.info('------------mergeFrame-------------')
    log.info(merge_frame)
    diff = merge_frame[merge_frame.isna().any(axis=1)]
    log.info('diffSize %s', len(diff))
    if (len(diff)) > 0:
        file_name = str(date.today()) + '/' + str(date.today()) + name + "差异数据.xlsx"
        mkdir(log, str(date.today()))
        export_sheet(log, diff, file_name)
