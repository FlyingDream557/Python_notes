#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Topic: 使用csv模块读写文件
'''


import csv
from collections import namedtuple


# 方法1，使用csv模块读写
def by_csv_reader1():
    '''
        此种方式 想要访问某个字段需要通过下标来访问.
    '''
    with open('working_hours.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)  # 去掉开始的字段行
        print(headers)
        print('--------------------------')
        for row in f_csv:
            print(row[5], row[6])



def by_csv_reader2():
    '''
        由于使用下标访问通常会引起混淆，所有可以考虑使用命令元祖
    '''
    with open('working_hours.csv') as f:
        f_csv = csv.reader(f)  
        headings = next(f_csv)  # 得到第一行的字段名
        Row = namedtuple('Row', headings)
        for r in f_csv:
            row = Row(*r)
            # print(row)
            print(row.首次打卡日期, row.末次打卡日期)

def by_csv_reader3():
    '''
        将数据读取到一个字典序列中
    '''
    with open('working_hours.csv') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            # print(row)  # 得到一个有序字典，可以通过列名来访问
            print(row['首次打卡日期'], row['末次打卡日期'])


def by_csv_writer1():
    '''
        将列表数据写入csv文件中
    '''
    
    headers = ['Symbol','Price','Date','Time','Change','Volume']
    rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
             ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
             ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
           ]

    with open('stocks.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
        # writerows等同于下面的
        # for row in rows:
            # f_csv.writerow(row)

def by_csv_writer2():
    '''
        将字典数据写入到csv文件中
    '''
    headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
    rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
            'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
            {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
            'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
            {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
            'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
            ]

    with open('stocks2.csv', 'w', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)

by_csv_reader1()
by_csv_reader2()
by_csv_reader3()
by_csv_writer1()
by_csv_writer2()




    
