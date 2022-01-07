#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Author : 王俊奇
# @Email : wjqi@histudy.com
import os
import unittest
from ddt import ddt, data, unpack
from .readexcel import ReadExcel
from  specialtest.批量导出报表 import downloadreport


@ddt
class TestRunReport(unittest.TestCase):
    headers = {"Accept": "application/json,",
               "Cookie": ""}
    excelpath = os.path.dirname(__file__) + "/导出数据参数.xlsx"
    exceldata = ReadExcel(excelpath).get_data()

    @data(*exceldata)
    @unpack
    def test_run_report(self, cookie, export_type, org_id, org_name, startime, endtime):
        if export_type == '业绩明细表':
            url = f"http://erp.histudy.com/report/common/performanceDetails/output?p_bu_id={org_id}&p_end_date={endtime}&p_start_date={startime}"
            self.headers["Cookie"] = cookie
            downloadreport.export_report(os.path.dirname(__file__)+"/filename", url, self.headers)
        elif export_type == '考勤消耗表':
            url = f"http://erp.histudy.com/report/common/attendance_output?default_range=lastWeek&p_branch_name=%E5%85%B6%E4%BB%96&p_bu_id={org_id}&p_business_type=1&p_end_date={endtime}&p_isCourseTime=false&p_start_date={startime}"
            self.headers["Cookie"] = cookie
            downloadreport.export_report(os.path.dirname(__file__)+"/filename", url, self.headers)
            print("执行业绩明细表导出")


if '__main__' == '__name__':
    unittest.main()
