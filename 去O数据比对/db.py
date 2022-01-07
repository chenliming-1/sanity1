#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2020-11-18 10:14
# -*- coding: utf-8 -*-

import configparser
import pymysql as mdb
import os
import cx_Oracle as ora
import sys
import pymysql.converters as conv
import threading



"""
单例模式获取数据连接
"""


def singleton(cls, *args, **kwargs):
    instances = {}

    def get_instance(*args, **kwargs):
        if args not in instances:
            instances[args] = cls(*args, **kwargs)
        return instances[args]

    return get_instance


"""
数据库操作
"""


def dao(db, sql):
    cur = Conn(db,threading.current_thread().name)
    # print(cur)
    if sql.lower().startswith("select"):
        return cur.query(sql)
    else:
        return cur.modify(sql)


@singleton
class Conn(object):
    sql = []
    db = None
    cursor = None

    # 初始化

    def __init__(self, dbname,threadname):
        # file = 'F:\\test_e2e\\tc_e2e\\Data\\db.conf'
        # file = os.path.join(os.path.dirname(sys.executable), 'lib', 'site-packages', 'histudy', 'db.conf')
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.conf")
        config = configparser.RawConfigParser()
        config.read(file)
        conf = config[dbname]
        db_type = conf['type']
        host = conf['host']
        port = conf['port']
        database = conf['database']
        user = conf['user']
        pwd = conf['pwd']

        if db_type == 'mysql':
            charset = conf['charset']
            # conv = conversions.copy()
            self.db = mdb.connect(host=host, port=int(port), user=user, passwd=pwd, db=database, charset=charset)
            self.cursor = self.db.cursor(cursor=mdb.cursors.DictCursor)
        if db_type == 'oracle':
            # 设置字符集
            os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
            self.db = ora.connect(user + '/' + pwd + '@' + host + ':' + port + '/' + database)
            self.cursor = self.db.cursor()
    # 关闭游标，关闭连接
    def __del__(self):
        self.cursor.close()
        self.db.close()

    # 查询数据
    def query(self, sql, count=0):
        if sql is not None and '' != sql:
            sql = sql.strip()

            # self.db.commit()
            self.cursor.execute(sql)
            # if int(count):
            #     return self.cursor.fetchmany(count)
            # else:
            #     return self.cursor.fetchall()
            if "pymysql" in str(type(self.cursor)):
                return self.cursor.fetchall()
            if "cx_Oracle" in str(type(self.cursor)):
                columns = [col[0] for col in self.cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in self.cursor.fetchall()
                ]

        else:
            print("sql is null")

    # 修改数据
    def modify(self, sql):
        if sql is not None and '' != sql:
            # print(sql)
            sql = sql.strip()
            self.cursor.execute(sql)
            self.db.commit()
        else:
            print("sql is null")

    # 执行sql文件
    def execfile(self, fname):
        resultList = []
        # 判断文件是否存在
        if os.path.exists(fname):
            file = open(fname, 'r', encoding='UTF-8')
            while 1:
                line = file.readline()
                if '' != line:
                    line = line.strip()
                    # 如果以select开头，调用查询的接口
                    if line.lower().startswith('select'):
                        resultList.append(self.query(line))
                    else:
                        self.modify(line)
                if not line:
                    break
                pass
            # 如果只有一条记录，返回
            if len(resultList) > 0:
                if len(resultList) == 1:
                    return resultList[0]
                else:
                    return resultList
            file.close()
        else:
            print(fname + " 文件不存在")


if __name__ == '__main__':
    print(dao("erp_ora", "select * from tab_student_info where id=100782346"))
    print(dao("erp_mysql", "select * from tab_student_info where id=100782346"))


