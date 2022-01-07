#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2019/7/24 18:29

import requests
from histudy import log

import xlrd,xlwt
import hashlib
url = {
    "erp": "http://erp.histudy.com",
}

def erp_course_server_post():
    readbook=xlrd.open_workbook("ERP未考勤数据.xls")
    table = readbook.sheet_by_name("王坤（2019-07-31）")
    col=4
    myWorkbook = xlwt.Workbook()
    mySheet = myWorkbook.add_sheet('request1212')
    for i in range(1,col):
        course_id = int(table.cell(i,0).value)
        seq = int(table.cell(i, 1).value)
        studentid = int(table.cell(i, 2).value)
        try:
            #生成sign，sign中的格式一定要与传入的request中的参数一致，否则会导致sign签名失败
            input = "name=1{\"courseId\": "+str(course_id)+",\"seq\": "+str(seq)+",\"studentInfos\": [{\"id\": "+str(studentid)+",\"attendType\": 12}]}" + "b01277e2353b4034b5db945a443c2563"   # get这个就是body
            server_sign = hashlib.md5(input.encode("utf-8")).hexdigest()
            datadict ="{\"courseId\": "+str(course_id)+",\"seq\": "+str(seq)+",\"studentInfos\": [{\"id\": "+str(studentid)+",\"attendType\": 12}]}"
            header={
                "Content-Type": "application/json"
            }
            openapi_url = f'{url["erp"]}/erp_openapi/stu_course/attend?name=1&sign='+server_sign
            response = requests.request( "POST",openapi_url, headers=header, data=datadict)
            status = response.json()["status"]
            message=response.json()["message"]
            if status == 200 or message == "操作成功":
                mySheet.write(i, 0, course_id)
                mySheet.write(i, 1, seq)
                mySheet.write(i, 2, studentid)
                mySheet.write(i, 3, openapi_url)
                mySheet.write(i, 4, datadict)
                mySheet.write(i, 5, response.text)
                log.info("调用open api服务接口成功,返回结果:"+response.text)
            else:
                mySheet.write(i, 0, course_id)
                mySheet.write(i, 1, seq)
                mySheet.write(i, 2, studentid)
                mySheet.write(i, 3, openapi_url)
                mySheet.write(i, 4, datadict)
                mySheet.write(i, 5, response.text)
                log.error("调用open api服务接口失败"+str(course_id))
        except Exception as error:
            log.error("调用课程服务接口失败,错误信息："f'{error}')
    myWorkbook.save("result1.xls")


def erp_course_server_get():
    try:
        input = "name=aaa" + "b01277e2353b4034b5db945a443c2563"   # get这个就是body
        server_sign = hashlib.md5(input.encode("utf-8")).hexdigest()
        print(server_sign)
        openapi_url = f'{url["erp"]}/erp_openapi/tr/userInfo?name=aaa8&sign={server_sign}'
        response = requests.get(openapi_url, "GET", headers=None, data=None)
        status = response.json()["status"]
        message=response.json()["message"]
        if status == 200 or message == "操作成功":
            log.info("调用open api服务接口成功,返回结果:"+response.text)
        else:
            log.error("调用open api服务接口失败")
    except Exception as error:
        log.error("调用课程服务接口失败,错误信息："f'{error}')



if __name__ == '__main__':
    erp_course_server_post()
