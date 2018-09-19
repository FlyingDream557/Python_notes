#!/usr/bin/env python3
# coding=utf-8

'''
name : Levi
date : 2018-5-30
email : lvze@tedu.cn
MODULE : python3.5 mysql pymysql
This is a dict project for AID 1803
'''

from socket import *
import os
import signal
import time
import pymysql
import sys

DICT_TEXT = './dict.txt'  # 全局变量，绑定文件路径
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)


# 主流程控制
def main():
    db = pymysql.connect('localhost', 'root',
                         '123456', 'dict')
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 忽略子进程退出
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            os_exit(0)
        except Exception:
            continue

        # 创建子进程
        pid = os.fork()
        if pid < 0:
            print("Create child process failed")
            c.close()
        elif pid == 0:
            s.close()
            do_child(c, db)
        else:
            c.close()
            continue


def do_child(c, db):
    # 循环接收请求
    while True:
        data = c.recv(128).decode()
        # print("Request:", data)

        if data[0] == 'R':
            do_register(c, db, data)
        elif data[0] == 'L':
            do_login(c, db, data)
        elif data[0] == 'E':
            c.close()
            sys.exit(0)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == 'H':
            do_history(c, db, data)


def do_register(c, db, data):
    print("执行注册操作")
    L = data.split(' ')
    name = L[1]
    passwd = L[2]
    cursor = db.cursor()

    sql = "select * from user where name='%s'" % name
    cursor.execute(sql)
    r = cursor.fetchone()
    if r is not None:
        c.send(b'EXISTS')
        return

    sql = "insert into user(name,passwd) values('%s','%s')" % (name, passwd)

    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception:
        c.send(b'FAIL')
        db.rollback()
        return
    else:
        print("注册成功")


def do_login(c, db, data):
    print("执行登录操作")
    L = data.split(' ')
    name = L[1]
    passwd = L[2]
    cursor = db.cursor()

    try:
        # select　查询操作时，不需要commit
        sql = "select * from user\
        where name='%s' and passwd='%s'" % (name, passwd)
        cursor.execute(sql)
        r = cursor.fetchone()
    except Exception:
        pass
    if r is None:
        c.send(b'FAIL')
    else:
        c.send(b'OK')


def do_query(c, db, data):
    print("执行查询操作")
    L = data.split(' ')
    name = L[1]
    word = L[2]
    cursor = db.cursor()
    print(data)

    # 插入历史记录
    def insert_history():
        # 生成当前时间
        tm = time.ctime()
        sql = "insert into hist(name, word, time) \
        values('%s','%s','%s')" % (name, word, tm)
        print(name, word, tm)

        try:
            cursor.execute(sql)
            db.commit()
        except Exception:
            db.rollback()
            return

    # 以下示意使用文件查询单词，可以通过数据库．会更方便
    try:
        f = open(DICT_TEXT, 'rb')
    except Exception:
        c.send(b'FAIL')
        return
    while True:
        print(data)
        line = f.readline().decode()
        if not line:
            c.send(b'FAIL')
            break
        tmp = line.split(' ')
        if tmp[0] > word:
            c.send(b'FAIL')
            # f.close()
            break
        if tmp[0] == word:
            c.send(b'OK')
            # 防止粘包
            time.sleep(0.1)
            c.send(line.encode())
            insert_history()
            break
    f.close()


def do_history(c, db, data):
    print('执行历史操作')
    name = data.split(' ')[1]
    cursor = db.cursor()
    try:
        sql = "select * from hist where name='%s'" % name
        cursor.execute(sql)
        r = cursor.fetchall()
        if not r:
            c.send(b'FAIL')
        else:
            c.send(b'OK')
    except Exception:
        pass
    for i in r:
        time.sleep(0.1)
        msg = '%s %s %s' % (i[1], i[2], i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')


if __name__ == '__main__':
    main()
