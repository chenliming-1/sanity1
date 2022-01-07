def get_sesion():
    session = "JSESSIONID=7F178A02C72A152837D7FCAD866B01A3;"
    return session


import xlrd
import os
import datetime


# 读取excel类
class ReadExcel(object):
    def __init__(self, excel, sheet=0):
        # 校验参数excel是否是有效的excel
        if os.path.exists(excel):
            self.excel = excel
        else:
            pass
            # raise FileNotFoundError("找不到excel文件....")
        self.sheet = sheet
        self._data = []

    def get_data(self):
        work_book = xlrd.open_workbook(self.excel)
        # 判断入参sheet的类型是int、或者str，sheet支持依据sheet_name或者index读取
        if isinstance(self.sheet, str):
            sheet_data = work_book.sheet_by_name(self.sheet)
        # sheet入参为index
        elif isinstance(self.sheet, int):
            sheet_data = work_book.sheet_by_index(self.sheet)
        else:
            raise TypeError("sheet传参仅支持int或string类型....")
        # 读取excel的总行数
        excel_rows = sheet_data.nrows
        # 读取excel的总列数
        excel_cols = sheet_data.ncols
        # 从非标题行开始遍历excel单元格数据
        for r in range(1, excel_rows):
            # 定义字典，用于存储excel数据
            excel_list = []
            for col in range(excel_cols):
                cell = sheet_data.cell_value(r, col)
                cell_type = sheet_data.cell_type(r, col)
                if cell_type == 2 and cell % 1 == 0.0:
                    cell = int(cell)
                    cell = str(cell)
                elif cell_type == 3:
                    cell = datetime.date(*xlrd.xldate_as_tuple(cell, work_book.datemode)[:3]).strftime('%Y-%m-%d')
                excel_list.append(cell)
            self._data.append(excel_list)
        return self._data
