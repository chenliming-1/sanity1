#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2021-01-13 14:53

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

def insertHiclassRoom(url, branch_id, room_name):
    headers = {"Cookie": str(get_sesion()), "Content-Type": "application/json"}
    response = request.run_main(url + "/erp/room/service", 'POST',
                                data={"branch_id": branch_id, "room_name": room_name, "room_num": "8",
                                      "room_position": room_name + "地址", "classroom_type": 2}, headers=headers)
    print(response.text)


def hiclassRoomBody(filename,sheetindex):
    excelpath = os.path.dirname(__file__) + filename
    exceldata = ReadExcel(excelpath, sheet=int(sheetindex)).get_data()
    env_url = "http://erp.histudy.com"
    for data in exceldata:
        # branch_name = data[1]
        # print(branch_name)
        # branch_id = dao(f'erp_prod', f"select id from tab_organization_info where org_name='{branch_name}'")[0]["ID"]
        branch_id=100002570
        teacher_name = data[1]
        class_room_name =teacher_name + "Hiclass教室"
        change_org(env_url, branch_id)
        import time
        time.sleep(1)
        insertHiclassRoom(env_url, branch_id, class_room_name)


hiclassRoomBody("/2021寒假培英班上课老师.xls",0)

