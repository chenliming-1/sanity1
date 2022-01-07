#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Author : 练素琼
# @Email : lsqiong_1@histudy.com
import os
import pandas
from 批量导出报表 import  export_report

def get_excel_data():
    excelpath = os.path.dirname(__file__) + "/导出数据参数.xlsx"
    df = pandas.read_excel(excelpath, sheet_name="Sheet1")
    for idx, row in df.iterrows():
        row_value = row.values
        cookie = row_value[0]
        bus_type = row_value[1]
        group_id = row_value[2]
        star_time = row_value[4]
        star_time_str = str(star_time)[0:10]
        end_time = row_value[5]
        end_time_str = str(end_time)[0:10]
        run_report(cookie, bus_type, group_id, star_time_str, end_time_str)


def run_report(cookie, export_type, org_id, startime, endtime):
    headers = {}
    if export_type == '业绩明细表':
        url = f"http://erp.histudy.com/report/common/performanceDetails/output?p_bu_id={org_id}&p_end_date={endtime}&p_start_date={startime}"
        headers["Cookie"] = cookie
        export_report(os.path.dirname(__file__) + "/filename","GET", url, headers)
    elif export_type == '考勤消耗表':
        url = f"http://erp.histudy.com/report/common/attendance_output?default_range=lastWeek&p_branch_name=%E5%85%B6%E4%BB%96&p_bu_id={org_id}&p_business_type=1&p_end_date={endtime}&p_isCourseTime=false&p_start_date={startime}"
        headers["Cookie"] = cookie
        export_report(os.path.dirname(__file__) + "/filename","GET", url, headers)
        print("执行业绩明细表导出")

    elif export_type == '考勤消耗表':
        url =""
        headers["Cookie"]= cookie
        export_report(os.path.dirname(__file__) + "/filename", "POST", url, headers,data={
            "aa":"xx",
        })


get_excel_data()
