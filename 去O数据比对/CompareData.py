#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2020-11-18 11:02

from db import dao
import re
import time
import cx_Oracle
import sys
import tables
import os

class CompareData():
    # 不用比较的表
    not_compare_tables = ['T_2018_RENEWAL_CURR_DETAIL', 'T_TEACHER_RANKING_LIST',
                          'DATA_JOY_BJK_TO_YDY', 'Y_TEACHER_SUBJECT_REF', 'Y_SCHOOL',
                          'Y_COMPANY_ACCOUNT', 'T_ORDER_COURSE_TIMES_LOG',
                          'Y_TEACHER2', 'V4_DXB_ATT', 'TV3_DATA_ATTENDGXH',
                          'Y_TEACHER', 'TAB_EMP_ORG_POST', 'WX_TIME_SEASON',
                          'WX_ORG_MENU', 'TV3_DATA_CHUNJIA', 'Y_DXB_ENTRY',
                          'Y_DXB_SUB_ENTRY', 'Y_DXB_SUB', 'Y_DXB', 'Y_COURSE_RIGHT',
                          'Y_COURSE_CNB', 'Y_COURSE_WFD', 'Y_COURSE_GXH', 'Y_COURSE_DXB',
                          'T_ASSTEACHER_WORKLOAD', 'TAB_GRADE_RELATION',
                          'T_GXH_STUDENT_STATUS_REPORT', 'JY_TMP', 'T_ORDER_CHANGE_REPORT',
                          'T_ORG_ACCOUNT_CASHIER', 'SYS_EXPORT_SCHEMA_01', 'MV_TEACHER_GROUP',
                          'PUB_USER_SCHOOL', 'XM_DXB_2015', 'TAB_SIGN_RECORD',
                          'T_2018_RENEWAL_LAST__DETAIL', 'MV_MTLASTSEASON_STUDENT_COUNTS',
                          'T_RENEWAL_ORDER_CHANGE', 'T_RENEWAL_CURR_ACTUAL_SNAPSHOT',
                          'T_RENEWAL_LAST_ACTUAL_SNAPSHOT', 'MV_MTLASTSEASON_STUDENT_DETAIL',
                          'T_RENEWAL_ACTUAL_DETAIL_2017', 'T_RENEWAL_LAST_MAXSTU_SNAPSHOT',
                          'T_RENEWAL_LAST_MAX_STUDENT', 'T_ORG_ACCOUNT_REPORT',
                          'T_RENEWAL_CURR_ACTUAL_DETAIL', 'T_RENEWAL_LAST_ACTUAL_DETAIL',
                          'MV_TEACHER_GROUP','TMP_TAB_STUDENT_INFO','TMP_TAB_EMPLOYEE_INFO',
                          'TAB_EAI_LOG_INFO','TMP_TAB_STUDENT_INFO_JOY','MV_TEACHER_GROUP','JBPM4_LOB'
                          ,'TAB_ORGANIZATION_INFO','T_RP_JY_COUNSELOR_ORDER'
                          ,'BUSINESS_OPERATE_LOG']
    list_context = []
    """
    写入文件
    """
    def write_result(self, context="",filename ='result.txt',init =0):
        filedir = os.path.join(os.path.split(os.path.realpath(__file__))[0],'logs')
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = os.path.join(filedir,filename)
        if(init == 1):
            file_handle = open(filename, mode='w+', encoding='utf-8')
            file_handle.truncate()
        else:
            file_handle = open(filename, mode='a+', encoding='utf-8')
        if str(context) not in self.list_context:
            self.list_context.append(context)
            file_handle.write(str(context) +'\n')
        file_handle.close()

    """
    获取对比的表
    """
    def get_compare_tables(self):
        return_list = []
        ora_tables = dao("erp_ora","select t.table_name from user_tables t where tablespace_name = 'KLFORM'  and table_name  not like '%BAK%' and table_name not like '%TEMP%' and "
                          "table_name != 'T_RP_JY_COUNSELOR_ORDER' and table_name  not like '%LOG%'  and table_name  not like '%LW%'"
                          "and NOT REGEXP_LIKE(TABLE_NAME, '.*?_[0-9]{4,8}$') and table_name  not like 'TMP_%'  and table_name "
                                   " not like 'MV_%' and table_name  not like 'V_%' AND TABLE_NAME NOT LIKE 'GUOHB_%' AND TABLE_NAME NOT LIKE 'JBPM4_%'"
                                   " AND TABLE_NAME NOT LIKE 'GC_%' ")
        for table in ora_tables:
            if table['TABLE_NAME'] not in self.not_compare_tables and table['TABLE_NAME'] not in tables.not_transfer_tables:
                return_list.append(table)

        return return_list

    """
    获取主键，有主键返回主键，
    主键返回 id列
    没有列名为ID的，不比较
    """
    def get_constraint(self,table_name):
        return_cloumn = ""
        constraint_column = dao("erp_ora",f"select cu.column_name from user_cons_columns cu, user_constraints au where cu.constraint_name = au.constraint_name and au.constraint_type = 'P' and au.table_name = '{table_name}'")
        if (len(constraint_column) > 0):
            return_cloumn = constraint_column[0]['COLUMN_NAME']
            return return_cloumn
        else:
            columns = dao("erp_ora",f"SELECT T.COLUMN_NAME FROM USER_TAB_COLUMNS T WHERE T.TABLE_NAME= '{table_name}'")
            for colum in columns:
                if colum['COLUMN_NAME'] == 'ID':
                    return_cloumn = 'ID'
                    return return_cloumn
            self.write_result(f"问题表,{table_name}有id没主键,返回查询列：{return_cloumn}")
            return return_cloumn

    """
    判断没有主键，但是有id且唯一的表
    """
    def get_not_exits_constraint_tables(self):
        # 排除的表,不比较
        table_no_compare =[
            'CLASS_WORK_RECORD',
            'GC_RESOURCE_HIS',
            'GC_RESOURCE_REC_HIS',
            'PLAN_TABLE',
            'PUB_COURSE',
            'T_ORDER_COURSE_LOG',
            'T_ORDER_COURSE_TIMES_LOG',
            'T_TEACHER_GROUP_ATTENDANCE',
            'TAB_EMP_ORG_POST',
            'TP_COURSE_GOAL',
            'WX_ORG_MENU'
        ]
        ora_tables = self.get_compare_tables()

        for table in ora_tables:
            file_name = "主键比对.txt"
            self.write_result("开始对比" + str(time.time()), file_name, 1)
            print(table['TABLE_NAME'])
            constraint_column = dao("erp_mysql",f"SELECT * FROM INFORMATION_SCHEMA.`KEY_COLUMN_USAGE` WHERE table_name='{table['TABLE_NAME']}'  and CONSTRAINT_SCHEMA='klform' and CONSTRAINT_name = 'PRIMARY'")
            if(len(constraint_column) ==0):
                columns = dao("erp_mysql",f"SELECT * FROM information_schema.columns WHERE table_name='{table['TABLE_NAME']}' and table_schema ='klform'")
                for column in columns:
                    if column['COLUMN_NAME']== 'ID' and table['TABLE_NAME'] not in table_no_compare:
                        self.write_result("问题表，{table['TABLE_NAME']},有id没主键",file_name)
                        # columns = dao("erp_mysql",f"SELECT id,count(1) FROM {table['TABLE_NAME']}' group by id having count(1) > 1")
                        # if (len(columns)) ==0:
                        #     print("问题表："+table['TABLE_NAME'])
        pass
    """
    查找异常的数据
    """
    def find_record(self,table1):
        file_name = "数据记录不一致查找.txt"
        self.write_result("主键比对" + str(time.time()), file_name, 1)

        table1_result = dao("erp_ora", f"select *  from  {table1}")
        cloumn = self.get_constraint(table1)
        for i in table1_result:
            result = dao("erp_mysql", f"select * from  {table1} where {cloumn} = {i[cloumn]}")
            if(len(result) == 0):
                self.write_result("问题表，{table1]},orcle有mysql没有，{cloumn} = {i[cloumn]}", file_name)
        table1_result = dao("erp_mysql", f"select *  from  {table1}")
        cloumn = self.get_constraint(table1)
        for i in table1_result:
            result = dao("erp_ora", f"select * from  {table1} where {cloumn} = {i[cloumn]}")
            if(len(result) == 0):
                self.write_result(f"问题表，{table1},mysql有erp没有，{cloumn} = {i[cloumn]}", file_name)

    """
    对比总行数
    """
    def compare_table_count(self):
        file_name = "总记录数比对"
        self.write_result("总记录数比对"+str(time.time()),file_name,1)
        # 比对总行数
        ora_tables = self.get_compare_tables();
        for table in ora_tables:
            oracle_count = dao("erp_ora", f"select count(1) as count from  {table['TABLE_NAME']}")
            mysql_count = dao("erp_mysql", f"select count(1) as count from  {table['TABLE_NAME']}")
            # print(table)
            if int(oracle_count[0]['COUNT']) > 300000:
                print(f"{table['TABLE_NAME']},{str(oracle_count[0]['COUNT'])}")
            if int(oracle_count[0]['COUNT']) != mysql_count[0]['count']:
                self.write_result(f"问题表,{table['TABLE_NAME']},记录数不一致， oracle的记录数： {str(oracle_count[0]['COUNT'])}   ；mysql记录数：  {str(mysql_count[0]['count'])}",file_name)

    def compare_column(self,table_name,ora_resulet1,constraint,filename1):
        for i in ora_resulet1:
            if 'ROWNO' in i.keys():
                i.pop('ROWNO')
            mysql_result = []
            try:
                mysql_result = dao("erp_mysql",f"select * from {table_name} where {constraint}= '{str(i[constraint])}' LIMIT 3")
            except Exception as e:
                self.write_result(f"问题表，{table_name}，mysql查询报错：{str(constraint)}={str(i[constraint])}",filename1)
                self.write_result(str(e), 'error.log')
            if (len(mysql_result) == 0 or mysql_result is None):
                self.write_result(f"问题表，{table_name}，mysql没数据：{str(constraint)}={str(i[constraint])}",filename1)
                continue
            elif (len(mysql_result) > 1):
                self.write_result(f"问题表，{table_name}，mysql存在多条记录：{str(constraint)}={str(i[constraint])}",filename1)
            else:
                self.write_result('mysql的结果，' + str(mysql_result), filename1)
                self.write_result('oracle的结果，' + str(i), filename1)
                for o_k, o_v in i.items():
                    if o_v is None:
                        if (mysql_result[0][o_k] is None):
                            pass
                        else:
                            self.write_result(f"问题表，{table_name}，不一致字段 ,{str(o_k)},oracle的值：{str(o_v)}，mysql的值，{str(mysql_result[0][o_k])} 具体的行{constraint}={str(i[constraint])}", filename1)
                    else:
                        if (type(o_v) == cx_Oracle.LOB or type(o_v) == cx_Oracle.CLOB):
                            continue
                        if str(o_v) != str(mysql_result[0][o_k]):
                            if o_k != "UPDATE_TIME":
                                if type(o_v) == float and float(o_v) != float(mysql_result[0][o_k]):
                                    if round(float(o_v), 5) == float(mysql_result[0][o_k]):
                                        pass
                                    else:
                                        # 再查一次精度
                                        scale = dao("erp_ora",f"select data_scale from user_tab_columns where Table_Name='{table_name}' and column_name = '{o_k}'")
                                        if round(float(o_v), int(scale[0]['DATA_SCALE'])) != float(
                                                mysql_result[0][o_k]):
                                            self.write_result(f"问题表，{table_naem}，不一致字段，{str(o_k)} ，mysql的值：{str(mysql_result[0][o_k])}，oracle的值，{str(i[o_k])} ， 具体的行 :{constraint}={str(i[constraint])}",filename1)
                                if type(o_v) == int:
                                    # 查询精度
                                    scale = dao("erp_ora",
                                                f"select data_scale from user_tab_columns where Table_Name='{table_name}' and column_name = '{o_k}'")
                                    if int(o_v) != int(mysql_result[0][o_k]):
                                        self.write_result("问题表，{table_name} ，不一致字段，{str(o_k)} ，mysql的值，{str(mysql_result[0][o_k])}， oracle的值，{str(i[o_k])} ， 具体的行,{constraint} =  {str(i[constraint])}",filename1)

                                    # orcle不带精度的，mysql转成保留5位小数，oralce有精度的根据精度来
                                    if len(str(mysql_result[0][o_k]).split(".")[1]) != 5 and len(
                                            str(mysql_result[0][o_k]).split(".")[1]) != int(scale[0]['DATA_SCALE']):
                                        self.write_result("问题表，{table_name}  ，不一致字段，{str(o_k)} ，mysql的值，{str(mysql_result[0][o_k])} ， oracle的值， {str(i[o_k])} ,具体的行 ， {constraint} ={str(i[constraint])}",filename1)


    def dataCompare(self,rownum_start,rownum_end,filename = 'reslut.txt'):
        self.write_result("开始对比",filename,1)

        rownum_start =str(rownum_start)
        rownum_end =str(rownum_end)
        start_time = time.time()
        self.write_result("开始对比"+str(start_time),filename,1)
        ora_tables = self.get_compare_tables()
        self.write_result("表的总数" + str(len(ora_tables)),filename)
        for table in ora_tables:
            if table['TABLE_NAME'] in self.not_compare_tables or  table['TABLE_NAME'] in tables.not_transfer_tables:
                continue
            self.write_result(f"比对表，{table['TABLE_NAME']} ，行数从 {rownum_start} 到{rownum_end}",filename)
            oracle_count = dao("erp_ora", f"SELECT count(1) as count FROM (SELECT ROWNUM AS rowno, t.*FROM {table['TABLE_NAME']} t WHERE ROWNUM <= {rownum_end}) table_alias WHERE table_alias.rowno >= {rownum_start}")
            if int(oracle_count[0]['COUNT']) == 0:
                continue
            ora_result = dao("erp_ora", f"SELECT * FROM (SELECT ROWNUM AS rowno, t.*FROM {table['TABLE_NAME']} t WHERE ROWNUM <= {rownum_end}) table_alias WHERE table_alias.rowno >= {rownum_start}")
            constraint = self.get_constraint(table['TABLE_NAME'])
            if(constraint == ""):
                continue
            for i in ora_result:
                if 'ROWNO' in i.keys():
                    i.pop('ROWNO')
                mysql_result = []
                try:
                    mysql_result = dao("erp_mysql", f"select * from {table['TABLE_NAME']} where {constraint}= '{str(i[constraint])}' LIMIT 3")
                except Exception as e:
                    self.write_result(f"问题表，{table['TABLE_NAME']}，mysql查询报错：{str(constraint)}={str(i[constraint])}",filename )
                    self.write_result(str(e),'error.log' )
                if (len(mysql_result) == 0 or mysql_result is None):
                    self.write_result(f"问题表，{table['TABLE_NAME']}，mysql没数据：{str(constraint)}={str(i[constraint])}",filename )
                    continue
                elif (len(mysql_result) > 1):
                    self.write_result(f"问题表，{table['TABLE_NAME']}，mysql存在多条记录：{str(constraint)}={str(i[constraint])}",filename )
                else:
                    # self.write_result('mysql的结果，'+str(mysql_result),filename)
                    # self.write_result('oracle的结果，'+str(i),filename)
                    self.write_result(f"开始比对，{table['TABLE_NAME']}，记录数：{oracle_count[0]['COUNT']}",filename )
                    for o_k, o_v in i.items():
                        if o_v is None:
                            if (mysql_result[0][o_k] is None):
                                pass
                            else:
                                self.write_result("问题表，" + table['TABLE_NAME'] + '，不一致字段，' + str(o_k) + "，oracle的值：" + str(
                                        o_v) + "  ，mysql的值，" + str(
                                        mysql_result[0][o_k]) + " 具体的行 ，" + constraint + " = " + str(
                                        i[constraint]),filename)
                        else:
                            if(type(o_v) == cx_Oracle.LOB or type(o_v) == cx_Oracle.CLOB):
                                continue
                            if str(o_v) != str(mysql_result[0][o_k]):
                                if  o_k != "UPDATE_TIME" :
                                    if type(o_v) == float and float(o_v) != float(mysql_result[0][o_k]):
                                        if round(float(o_v), 5) == float(mysql_result[0][o_k]):
                                            print(table['TABLE_NAME'])
                                            pass
                                        else:
                                            # 再查一次精度
                                            scale = dao("erp_ora",f"select data_scale from user_tab_columns where Table_Name='{table['TABLE_NAME']}' and column_name = '{o_k}'")
                                            # print(str(scale[0]['DATA_SCALE']))
                                            # print(str(round(float(o_v), int(scale[0]['DATA_SCALE']))))
                                            # print(str(float(mysql_result[0][o_k])))
                                            if round(float(o_v), int(scale[0]['DATA_SCALE'])) != float(mysql_result[0][o_k]):
                                                self.write_result("问题表，" + table['TABLE_NAME'] + '，不一致字段，' + str(
                                                    o_k) + "，mysql的值：" + str(mysql_result[0][o_k]) + "，oracle的值，" + str(
                                                    i[o_k]) + "， 具体的行 :" + constraint + " = " + str(i[constraint]),filename)
                                    if type(o_v) == int:
                                        # 查询精度
                                        scale = dao("erp_ora", f"select data_scale from user_tab_columns where Table_Name='{table['TABLE_NAME']}' and column_name = '{o_k}'")
                                        if int(o_v) != int(mysql_result[0][o_k]):
                                            self.write_result("问题表，" + table['TABLE_NAME'] + ' ，不一致字段，' + str(o_k) + "，mysql的值，" + str(mysql_result[0][o_k]) + "， oracle的值，" + str(i[o_k]) + "， 具体的行 ，" + constraint + " = " + str(i[constraint]), filename)

                                        # orcle不带精度的，mysql转成保留5位小数，oralce有精度的根据精度来
                                        if len(str(mysql_result[0][o_k]).split(".")[1]) !=5 and  len(str(mysql_result[0][o_k]).split(".")[1]) !=int(scale[0]['DATA_SCALE']):
                                            self.write_result("问题表，" + table['TABLE_NAME'] + ' ，不一致字段，' + str(o_k) + "，mysql的值，" + str(mysql_result[0][o_k]) + "， oracle的值，" + str(i[o_k]) + "， 具体的行 ，" + constraint + " = " + str(i[constraint]), filename)


        self.write_result("结束比对 耗时" + str(time.time()-start_time),filename)


if __name__ == '__main__':
    start_num =  sys.argv[1]
    end_num =  sys.argv[2]
    print(str(start_num))
    print(str(end_num))
    compare1 = CompareData()
    # compare1.find_record('TAB_USER_ROLE_REF')
    # compare1.compare_table_count()
    # compare1.get_compare_tables()

    #
    # for i in compare1.not_compare_tables:
    #     if i not in tables.not_transfer_tables:
    #         print(i)
    # compare1.get_not_exits_constraint_tables()

    compare1.dataCompare(start_num,end_num,f"result_{start_num}_{end_num}.txt")










