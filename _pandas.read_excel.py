# import pandas.read_excel
# !/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
import numpy as np
from pandas import DataFrame
import uuid
import time
import threading

title1 = []
title2 = []


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def file_detect(file_name):
    fr = open(file_name, 'rb')
    buf = fr.read(4)
    if buf == b'%TSD':
        bu = 0
        print('文件格式不支持')
    if buf == b'\xd0\xcf\x11\xe0' or buf == b'PK\x03\x04':
        bu = 1
    else:
        bu = 2
        print('文件格式不支持')
    fr.close()
    return bu


def sheet_detect(file_name, num):
    df1 = pd.ExcelFile(file_name)
    sheet = len(df1.sheet_names)
    if sheet > 1:
        print(str(num) + ' bom 有 ' + str(sheet) + ' 个 sheet')
    return sheet


def title_split(name1, name2):
    # df1 = pd.ExcelFile(name)
    # sheet_names[0]：第一张工作表名称    0：第一张；1：第二张；......
    # title = [df1.sheet_names[0].split('_')[2]]
    df1 = pd.read_excel(name1)
    title1.append([])
    title1[0].append(str(df1.values[0][4]) + '组装阶')
    i = 0
    for j in range(0, len(df1)):
        df1.fillna(0, inplace=True)
        if df1.values[j][3] != 0:
            i = i + 1
            title1.append([])
            title1[i].append(df1.values[j][4])
    df2 = pd.read_excel(name2)
    title2.append([])
    title2[0].append(str(df2.values[0][4]) + '组装阶')
    i = 0
    for j in range(0, len(df2)):
        df2.fillna(0, inplace=True)
        if df2.values[j][3] != 0:
            i = i + 1
            title2.append([])
            title2[i].append(df2.values[j][4])

    return


'''
file_split：     将bom分层生成新文件

'''


def file_split(self, name, title):
    df = pd.read_excel(name)
    bom = np.split(df, *np.where(df.项目编号.isnull()))
    for j in range(0, len(bom)):
        filename = str(title[j]) + self + '.xlsx'
        bom[j].to_excel(filename, encoding='utf-8')

    return bom


'''
bom_add:bom
'''


def bom_add(self1, name1, self2, name2, Column_name):
    uuid_str = uuid.uuid4().hex
    tmp_file_name = 'tmpfile/tmpfile_%s.wav' % uuid_str
    tmp_f_path = os.path.join(os.getcwd(), tmp_file_name)
    fw = open(tmp_f_path, 'w')
    bom1 = file_split(self1, name1, title1)
    bom2 = file_split(self2, name2, title2)
    fw.write(' ' + '\t' + '\t' + '\t' + '\t' + '\t' + '\n')
    for j in range(0, len(bom1)):
        bom1[j] = bom1[j].append(bom2[j])
        bom1[j] = bom1[j].append(bom2[j])
        bom1[j] = bom1[j].drop_duplicates(subset=Column_name, keep=False)

        if len(bom1[j].values) == 0:
            pass
        else:
            title = title1
            bom = bom1[j][['对象标识', '菲菱子件用量', '位号']]
            bom = bom.reindex(columns=[' ', '对象标识', '菲菱子件用量', '位号'])
            bom.iat[0, 0] = str(title[j])
            bom = bom.where(bom.notnull(), '   ')

            for line in bom.values:
                fw.write('\t')
                for i in range(0, 4):
                    fw.write(str(line[i]) + '\t')
                fw.write('\n')
    fw.close()
    return tmp_f_path


def bom_del(self1, name1, self2, name2, Column_name):
    uuid_str = uuid.uuid4().hex

    tmp_file_name = 'tmpfile/tmpfile_%s.wav' % uuid_str
    tmp_f_path = os.path.join(os.getcwd(), tmp_file_name)
    fw = open(tmp_f_path, 'w')
    bom1 = file_split(self1, name1, title1)
    bom2 = file_split(self2, name2, title2)
    fw.write(' ' + '\t' + '\t' + '\t' + '\t' + '\t' + '\n')
    for j in range(0, len(bom1)):
        bom2[j] = bom2[j].append(bom1[j])
        bom2[j] = bom2[j].append(bom1[j])
        bom2[j] = bom2[j].drop_duplicates(subset=Column_name, keep=False)
        if len(bom2[j].values) == 0:
            pass
        else:
            title = title2
            bom2[j] = bom2[j].where(bom2[j].notnull(), '   ')
            bom = bom2[j][['对象标识', '菲菱子件用量', '位号']]
            bom = bom.reindex(columns=[' ', '对象标识', '菲菱子件用量', '位号'])
            bom.iat[0, 0] = str(title[j])
            bom = bom.where(bom.notnull(), '   ')
            for line in bom.values:
                fw.write('\t')
                for i in range(0, 4):
                    fw.write(str(line[i]) + '\t')
                fw.write('\n')
    fw.close()
    return tmp_f_path


def read_txt(name):
    data = []
    with open(name, 'r') as df:
        # 读每一行
        for line in df:
            line = str(line).split('\t')
            data.append(line)
    df = DataFrame(data)
    # print(df)
    return df


def merge_file(self1, name1, self2, name2, Column_name):
    new = read_txt(bom_add(self1, name1, self2, name2, Column_name))
    old = read_txt(bom_del(self1, name1, self2, name2, Column_name))
    new.drop(new.columns[5], axis=1, inplace=True)
    old.drop(old.columns[5], axis=1, inplace=True)
    new.columns = ['结果', '半成品层', '编码', '数量A', '位号A']
    old.columns = ['结果', '半成品层', '编码', '数量B', '位号B']
    df = pd.merge(new, old, on=['结果', '半成品层', '编码'], how='outer')
    df = df.where(df.notnull(), '   ')  # 将空值nan改为空
    os.remove(bom_add(self1, name1, self2, name2, Column_name))
    os.remove(bom_del(self1, name1, self2, name2, Column_name))
    return df


'''
row_test:        新bom旧bom 行比对

'''


def row_test(self1, name1, self2, name2):
    row = merge_file(self1, name1, self2, name2, ['级别', '对象标识'])
    for i in range(0, len(row)):
        if row.values[i][3] == '   ' and row.values[i][4] == '   ':
            row.values[i][0] = '删除'
        if row.values[i][5] == '   ' and row.values[i][6] == '   ':
            row.values[i][0] = '增加'
    row = row.drop(index=0)  # 删掉第一行空行
    return row


'''
tag_pcs_test:        新bom旧bom 数量位号比对

'''


def tag_pcs_test(self1, name1, self2, name2):
    tp = merge_file(self1, name1, self2, name2, ['对象标识', '位号', '菲菱子件用量'])
    tp = tp.drop(index=0)
    tag_pcs = tp.drop(index=(tp.loc[(tp['数量A'] == '   ') & (tp['位号A'] == '   ')].index))
    tag_pcs = tag_pcs.drop(index=(tag_pcs.loc[(tag_pcs['数量B'] == '   ') & (tag_pcs['位号B'] == '   ')].index))
    for i in range(0, len(tag_pcs)):
        if float(tag_pcs.values[i][3]) == float(tag_pcs.values[i][5]):
            tag_pcs.values[i][0] = '位号不匹配'
        else:
            tag_pcs.values[i][0] = '数量不匹配'

    for i in range(0, len(tag_pcs)):
        A = tag_pcs.values[i][4]
        B = tag_pcs.values[i][6]
        A = A.split(',')
        B = B.split(',')
        c = list(set(A).difference(set(B)))
        d = list(set(B).difference(set(A)))
        tag_pcs.values[i][4] = ','.join(c)
        tag_pcs.values[i][6] = ','.join(d)
    return tag_pcs


'''
tag_check:        新bom 验证位号准确性

A面位号+B面位号=位号 
'''


def tag_check(self1, name1):
    error = []
    df1 = file_split(self1, name1, title1)
    title = title1
    for j in range(0, len(df1)):
        for i in range(0, len(df1[j])):
            df1[j].fillna(0, inplace=True)  # 如果df1为空值填充0
            error.append([])
            if df1[j].values[i][15] == 0:
                if df1[j].values[i][13] != 0 or df1[j].values[i][14] != 0:
                    error[j].append(' ' + str(df1[j].values[i][4]) + ' ' + str(df1[j].values[i][13]) + ' ' + str(
                        df1[j].values[i][14]) + ' ' + str(df1[j].values[i][15]))
            else:
                if df1[j].values[i][13] != 0 and df1[j].values[i][14] != 0:
                    tup1 = len(df1[j].values[i][13].split(','))
                    tup2 = len(df1[j].values[i][14].split(','))
                    tup3 = len(df1[j].values[i][15].split(','))
                    if tup1 + tup2 != tup3:
                        error[j].append(' ' + str(df1[j].values[i][4]) + ' ' + str(df1[j].values[i][13]) + ' ' + str(
                            df1[j].values[i][14]) + ' ' + str(df1[j].values[i][15]))
                else:
                    if df1[j].values[i][14] != 0 and df1[j].values[i][13] == 0:
                        tup2 = len(df1[j].values[i][14].split(','))
                        tup3 = len(df1[j].values[i][15].split(','))
                        if tup2 != tup3:
                            error[j].append(
                                ' ' + str(df1[j].values[i][4]) + ' ' + str(df1[j].values[i][13]) + ' ' + str(
                                    df1[j].values[i][14]) + ' ' + str(df1[j].values[i][15]))
                    if df1[j].values[i][13] != 0 and df1[j].values[i][14] == 0:
                        tup1 = len(df1[j].values[i][13].split(','))
                        tup3 = len(df1[j].values[i][15].split(','))
                        if tup1 != tup3:
                            error[j].append(
                                ' ' + str(df1[j].values[i][4]) + ' ' + str(df1[j].values[i][13]) + ' ' + str(
                                    df1[j].values[i][14]) + ' ' + str(df1[j].values[i][15]))
        if error[j]:
            for i in range(0, len(error[j])):
                error[j][i] = error[j][i].split(' ')
                error[j][i] = ['  ' if (i == '0' or i == '0.0') else i for i in error[j][i]]
                A = error[j][i][2]
                B = error[j][i][3]
                C = error[j][i][4]
                A = A.split(',')
                B = B.split(',')
                C = C.split(',')
                a = list(set(A).difference(set(C)))
                b = list(set(B).difference(set(C)))
                a_b = list(set(A).union(set(B)))
                c = list(set(C).difference(set(a_b)))
                error[j][i][2] = ','.join(a)
                error[j][i][3] = ','.join(b)
                error[j][i][4] = ','.join(c)
            error[j][0][0] = (title[j])
    while [] in error:
        error.remove([])
    return error


'''
tag_pcs_check:        新bom 验证位号和数量的关系

位号的总数量=菲菱子件用量（数量）
'''


def tag_pcs_check(self1, name1):
    error = []
    df1 = file_split(self1, name1, title1)
    title = title1
    for j in range(0, len(df1)):
        error.append([])
        for i in range(0, len(df1[j])):
            df1[j].fillna(0, inplace=True)  # 如果df1为空值填充0
            if df1[j].values[i][15] == 0:
                i = i + 1
            else:
                tup = tuple(df1[j].values[i][15].split(','))
                if len(tup) != df1[j].values[i][11]:
                    error[j].append(' ' + str(df1[j].values[i][4]) + ' ' + str(df1[j].values[i][11]) + ' ' + str(
                        df1[j].values[i][15]))

        if error[j]:
            for i in range(0, len(error[j])):
                error[j][i] = error[j][i].split(' ')
                error[j][i] = ['  ' if (i == '0' or i == '0.0') else i for i in error[j][i]]

            error[j][0][0] = title[j]
    while [] in error:
        error.remove([])
    return error


'''
bot_tag_pcs_check:        新bom 验证相同替代组的的位号&数量

相同替代组的的位号相同，数量相同
'''


def bot_tag_pcs_check(self1, name1):
    df = file_split(self1, name1, title1)
    title = title1
    error = []
    for j in range(0, len(df)):
        df[j] = df[j][['对象标识', '替代项目组', '菲菱子件用量', '位号']]
        df[j] = df[j].reindex(columns=['半成品层', '对象标识', '替代项目组', '菲菱子件用量', '位号'])
        df[j].iat[0, 0] = str(title[j])
        error.append([])
        sj = df[j][df[j]['替代项目组'].notna()]
        bot = sj['替代项目组'].unique()

        for i in bot:
            date = sj[sj['替代项目组'].isin([i])]
            date.iat[0, 0] = str(title[j])
            tag = date['位号'].unique()
            pcs = date['菲菱子件用量'].unique()
            if len(tag) > 1 or len(pcs) > 1:
                # print (date['对象标识','替代项目组','菲菱子件用量','位号']])
                date = date.where(date.notnull(), '   ')
                error[j].append(date)

    while [] in error:
        error.remove([])

    return error


'''
bot_use:        新bom 验证相同替代组的使用可能性

相同替代组的使用可能性=100
'''


def bot_use(self1, name1):
    df = file_split(self1, name1, title1)
    title = title1
    error = []
    for j in range(0, len(df)):
        df[j] = df[j][['对象标识', '替代项目组', '使用可能性']]
        df[j] = df[j].reindex(columns=['半成品层', '对象标识', '替代项目组', '使用可能性'])
        df[j].iat[0, 0] = str(title[j])
        error.append([])
        sj = df[j][df[j]['替代项目组'].notna()]
        bot = sj['替代项目组'].unique()

        for i in bot:
            date = sj[sj['替代项目组'].isin([i])]
            date.iat[0, 0] = str(title[j])
            use = pd.pivot_table(date, index=['替代项目组'], values=['使用可能性'], aggfunc='sum')
            if use.values != 100:
                date = date.where(date.notnull(), '   ')
                error[j].append(date)
    while [] in error:
        error.remove([])
    return error


'''
del_file：删除分层文件
'''


def del_file(self, name, title):
    df = pd.read_excel(name)
    bom = np.split(df, *np.where(df.项目编号.isnull()))
    for j in range(0, len(bom)):
        title3 = title
        filename = str(title3[j]) + self + '.xlsx'
        if os.path.exists(filename):
            os.remove(str(title3[j]) + self + '.xlsx')
    title.clear()


def All_del(self1, name1, self2, name2):
    del_file(self1, name1, title1)
    del_file(self2, name2, title2)

    return

# 输入新bom：1.xls，旧bom：2.xls
# All_Test ('new','1.xls','old','2.xls')
# 命令行输入
# All_Test ('new',input('请输入A BOM文件名:'),'old',input('请输入B BOM文件名:'))
