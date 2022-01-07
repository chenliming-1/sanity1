#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2019/3/6 18:29

from histudy import request, send, log
from commidware.recognize.driver import get_login_driver
# import hashlib
# import os
import re
url = {
    # ERP
    "erp": "https://erp.histudy.com",
    # 加盟商
    "alliance": "https://v6.histudy.com",
    "alliance_manage": "https://v6.histudy.com",
    # TA移动端
    "mobile": "https://m-erp.histudy.com",
    # 人才
    "tc_manager": "http://manage.tc.histudy.com",
    "tc_staff": "http://staff.tc.histudy.com",
    "tc_teacher": "http://teacher.tc.histudy.com",
    # 教研
    "tr_teacher": "https://tr.histudy.com",
    "tr_manage": "https://manage-tr.histudy.com",
    "tr_tools": "https://st.histudy.com",
    # HRM
    "hrm": "https://hrm.histudy.com",
    # 官网
    "index": "https://www.histudy.com",
    # OA
    "oa": "https://oa.histudy.com",
    # 家长端小程序
    "small_parents": "https://parents.mp.histudy.com",
    # cas的跳转页
    "sso": "https://sso.histudy.com"
}


def erp_openapi_check():
    try:
        # input = "name=aaa" + "b01277e2353b4034b5db945a443c2563"
        # server_sign = hashlib.md5(input.encode("utf-8")).hexdigest()
        # print(server_sign)
        openapi_url = f'{url["erp"]}/erp_openapi/tr/userInfo?name=klxx_checkapi'
        response = request.run_main(openapi_url, "GET", headers=None, data=None)
        status = response.json()["status"]
        message=response.json()["message"]
        if status == 200 or message == "操作成功":
            log.info("调用open api服务接口成功,返回结果:"+response.text)
        else:
            log.error("调用open api服务接口失败")
    except Exception as error:
        log.error("调用课程服务接口失败,错误信息："f'{error}')


def erp_order_server(cookie):
    order_url = f'{url["erp"]}/erp/ordermanager/service?order_id=0'
    header = {
        "Cookie": cookie,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        response = request.run_main(order_url, "GET", headers=header, data=None)
        response_order = response.json()['message']
        if response_order == "异常:订单不存在!":
            log.info("调用订单服务接口成功,返回结果:" + response.text)
        else:
            log.error("调用订单服务接口失败")
    except Exception as error:
        log.error("调用订单服务接口失败,错误信息："f'{error}')


def erp_hrm_server(cookie):
    hrm_url = f'{url["erp"]}/hrm/hrmSystemSettings/hrmAccountMgr/queryRoleWithAccount?user_id=111'
    header = {
        "Cookie": cookie,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        response = request.run_main(hrm_url, "GET", headers=header, data=None)
        response_orgservice = response.json()
        if "message" in response_orgservice:
            log.info("调用人员服务接口成功,返回结果:" + response.text)
        else:
            log.error("调用人员服务接口失败")
    except Exception as error:
        log.error("调用人员服务接口失败,错误信息："f'{error}')


def erp_report_server(cookie):
    hrm_url = f'{url["erp"]}/gxhcrm/report/queryPage/channelPage?p_grp_company=true&p_grp_sch=true&p_bu_id=12&p_branch_id=-1&p_channel_code=&p_start_date=&p_end_date=&rows=10&page=1'
    header = {
        "Cookie": cookie,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        response = request.run_main(hrm_url, "GET", headers=header, data=None)
        response_report = response.json()
        if "rows" in response_report:
            log.info("调用报告服务接口成功,返回结果:" + response.text)
        else:
            log.error("调用报告服务接口失败")
    except Exception as error:
        log.error("调用报告服务接口失败,错误信息："f'{error}')



def klxx_server():
    for i in url:
        response = request.run_main(url=url[i], method='GET', headers=None, data=None)
        matchRe = re.match(r"^[4|5]\d{2}", str(response.status_code))  # None为不是4开头或者5开头的，所以可以
        if matchRe != None:
            content = "请求的URL为：" + url[i] + "\n"
            content += "请求的错误码为：" + str(response.status_code) + "\n,"
            # content += "攻城狮，收到此邮件，请尽快确认系统是否可正常访问及修复！！"
            # emailaddress = os.getenv("emailaddress")
            # if emailaddress == None:
            #     emailaddress = 'lsqiong_1@histudy.com', 'guohb_histudy.com', 'cgxiang@histudy.com', 'wjqi@histudy.com', 'xcyuan@histudy.com','gongyq@histudy.com'
            # send.sendemail("DNS监控域名解析错误报告", content, emailaddress, attachment=None)
            log.error(content)
        else:
            log.info(url[i] + " 请求成功！请求返回的状态码:" + str(response.status_code))



if __name__ == '__main__':
    bw, cookie = get_login_driver("lsqiong_1", "Lsq4590578!", f'{url["erp"]}')
    erp_openapi_check()
    erp_order_server(cookie)
    erp_hrm_server(cookie)
    erp_report_server(cookie)
    klxx_server()
