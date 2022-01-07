#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2021-01-14 15:45
import time

body = {"needReSched": "N", "course_kind": "14", "sub_course_kind": "23", "sub_course_kind_name": "串讲课程",
        "cycle_type": "1", "product_type": 1, "course_name": "【Hiclass体验课】合肥培英班2021寒假曹雅婷老师", "subject_id": 2841,
        "attend_class_period": "1,2,3,4,5,6,7", "grade_id": 28, "season_id": 100016737, "unit_price": 150,
        "course_count": 7, "people_count": 100, "promotion_amount": 0, "start_date": "2021-01-15",
        "end_date": "2021-01-21", "start_time": "14:00", "end_time": "20:00", "hour_len": "6.00",
        "teacher_id": 100050014, "teacher_code": "cyting_3", "teacher_name": "曹雅婷", "performance_belong_type": 2,
        "branch_id": 100002110, "course_kind_name": "体验课", "saleMethod": "1", "saleMethodName": "仅ERP售卖",
        "class_level": "NONE", "has_textbook": 0, "is_assessment": "N", "subject_name": "其他", "grade_name": "其他",
        "cycle_type_name": "一期", "online_textbook_amount": "", "express_mode": "", "business_type": 1}

from common import ReadExcel, get_sesion
import os
from histudy import dao, request, log


# 切换团队
def change_org(url, branch_id):
    try:
        branch_id = int(branch_id)
        log.info("运行切换校区接口，切换至校区为：{0}的校区".format(branch_id))
        changeorg_rsp = request.run_main(
            url + "/common/orgservice?id=%d" % int(branch_id), 'PUT',
            data={},
            headers={"Cookie": str(get_sesion()), "Content-Type": "application/json"})
        rsp_error = changeorg_rsp.json()['error']
        rsp_changeTeam = changeorg_rsp.json()['changeTeam']
        print(rsp_changeTeam)
    except Exception as ex:
        log.error("切换校区异常，失败原因为：{0}".format(ex))
    finally:
        log.info("切换成功！")


# 创建教室

# url:=http://erp-aliyun.rls.klxuexi.net/erp/room/service
# 参数：{"branch_id":44,"room_name":"教室名称","room_num":"111","room_position":"教室地址","classroom_type":2}

def create_pyb_ke(url, city_name, teacher_name):
    headers = {"Cookie": str(get_sesion()), "Content-Type": "application/json"}
    body["course_name"] = "【Hiclass体验课】" + city_name + "培英班2021寒假" + teacher_name + "老师"
    body["teacher_name"]=teacher_name
    teacher_code =dao("erp_prod",f"select encoding from tab_teacher_info where teacher_name='{teacher_name}'")[0]["ENCODING"]
    teacher_id=dao("erp_prod",f"select id from tab_teacher_info where encoding='{teacher_code}'")[0]["ID"]
    body["teacher_id"] = teacher_id
    body["teacher_code"]=teacher_code
    response = request.run_main(url + "/erp/coursemanagerment/service", 'POST',
                                data=body, headers=headers)
    time.sleep(3)
    print(response.text)


def create_pyb_class(filename,sheetindex):
    excelpath = os.path.dirname(__file__) +filename
    exceldata = ReadExcel(excelpath, sheet=int(sheetindex)).get_data()
    env_url = "http://erp.histudy.com"
    for data in exceldata:
        # branch_name = data[1]
        # print(branch_name)
        # branch_id = dao(f'erp_prod', f"select id from tab_organization_info where org_name='{branch_name}'")[0]["ID"]
        branch_id = int(data[1])
        teacher_name = data[4]
        change_org(env_url, branch_id)
        city_name = data[0]
        time.sleep(3)
        create_pyb_ke(env_url, city_name, teacher_name)


# create_pyb_class("/培英班寒假老师统计.xlsx",4)
