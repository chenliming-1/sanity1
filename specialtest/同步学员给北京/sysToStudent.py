#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!@Author: 练素琼
#!Email: lsqiong_1@histudy.com
#!Date: 2019/7/31 14:10

import requests
from histudy import log,request

import xlrd,xlwt

import hashlib
from commidware.recognize.driver import get_login_driver

url = {
    "erp": "http://erp.histudy.com",
}



def erp_systostudent(cookie):
    readbook=xlrd.open_workbook("处理线上同步学生.xls")
    table = readbook.sheet_by_name("Sheet1")
    col=1733
    myWorkbook = xlwt.Workbook()
    mySheet = myWorkbook.add_sheet('request1')
    for i in range(1,col):
        student_id = int(table.cell(i,0).value)
        try:
            header={
                "Cookie": cookie,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            datadict = {
                "id":student_id
            }
            sys_stuednt_url = f'{url["erp"]}/erp/studentservice/synToDouble'
            response = request.run_main( sys_stuednt_url,"POST", headers=header, data=datadict)
            print(response.text)
            status = response.json()["error"]
            print(status)
            if status == False:
                mySheet.write(i, 0, student_id)
                mySheet.write(i, 1, response.text)
                log.info("调用同步学员接口成功,返回结果:"+response.text)
            else:
                mySheet.write(i, 0, student_id)
                mySheet.write(i, 1, response.text)
                log.error("调用open api服务接口失败"+str(student_id))
        except Exception as error:
            log.error("调用课程服务接口失败,错误信息："f'{error}')
        finally:
            myWorkbook.save("全部失败后再次同步结果.xls")


if __name__ == '__main__':
    bw, cookie = get_login_driver("lsqiong_1", "Lsq4590578!", f'{url["erp"]}')
    erp_systostudent(cookie)