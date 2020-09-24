#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: data_base.py
@time: 2020/9/22 13:21
@desc:
"""
import dmPython

class DataBase:
    def __init__(self):
        user = 'SYSDBA'
        password = 'citygis1613'
        server = '106.14.243.179'
        port = 5236

        try:
            conn = dmPython.connect(
                user=user,
                password=password,
                server=server,
                port=port,
                autoCommit=True
            )
            print("数据库连接成功！")
            self.conn = conn
        except dmPython.Error as e:
            print("连接失败", str(e))

    def create_tb(self, sql):
        try:
            cursor = self.conn.cursor()  # 获取光标
            cursor.execute(sql)  # 执行sql
            print("创建成功")
        except dmPython.Error as e:
            print("创建失败", str(e))
        finally:
            cursor.close()  # 关闭游标

    def insert_tb(self, sql, data):
        try:
            cursor = self.conn.cursor()
            cursor.executemany(sql, data)
            self.conn.commit()
            print("数据插入成功")
        except dmPython.Error as e:
            self.conn.rollback()
            print("插入失败", str(e))
        finally:
            cursor.close()

    def select_tb(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result1 = cursor.fetchall()
            # print("查询全部结果：", result1)
            return result1
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()

    def select_tb_one(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result2 = cursor.fetchone()
            print("查询一条结果：", result2)
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()

    def select_tb_many(self, sql, count):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result3 = cursor.fetchmany(count)
            print("查询结果：", result3)
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()

    def update(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            print("修改成功")
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()