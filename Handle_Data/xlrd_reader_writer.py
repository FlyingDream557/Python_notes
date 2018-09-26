#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Topic: 使用xlrd操作Excel的读写
Desc:
    csv是文本文件,用记事本就能打开，
    而xls是二进制的文件只有用EXCEL才能打开
'''

import xlrd

def read_file():

    # 1.打开Excel文件读取数据
    data = xlrd.open_workbook('test.xlsx')

    # 2.获取一个工作表
    # table = data.sheets()[0]  # 通过索引顺序获取
    table = data.sheet_by_index(0)  # 通过索引顺序获取
    # table = data.sheet_by_name(u'Sheet2')  # 通过名称获取

    # 3.获取整行和整列的值 (数组)
    # row = table.row_values(5)
    # print(row)
    # col = table.col_values(4)
    # print(col)

    # 4.获取行数和列数
    nrows = table.nrows
    ncols = table.ncols
    print(nrows, ncols)    

    # 5.循环行列表数据
    for i in range(nrows):
        print(table.row_values(i))

    # 6.单元格
    cell_A1 = table.cell(0, 0).value
    cell_C4 = table.cell(2, 3).value
    print(cell_A1, cell_C4)

    # 7.使用行列索引
    cell_A1 = table.row(0)[0].value
    cell_A2 = table.col(1)[0].value
    print(cell_A1, cell_A2)


read_file()
