#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2021-01-22 9:24
import requests
from specialtest import common
import json


class Recharge(object):
    def __init__(self):
        self.url = "http://erp-aliyun.rls.klxuexi.net/"
        self.data = {"studentId": "100714555", "payAmount": "1"}
        self.header = {
            "Content-Type": "application/json;charset=UTF-8",
            "cookie": common.get_sesion()
        }

    def recharhge(self):
        response = requests.post(f"{self.url}erp/2ta/h5/order/recharge/share-code/re-create",
                                 data=json.dumps(self.data), headers=self.header)
        print(response.text)

    def invalid(self):
        result = requests.post(f"{self.url}erp/2ta/h5/order/recharge/share-code/{self.data['studentId']}/invalid",
                               data=json.dumps(self.data), headers=self.header)
        print(result.text)


if __name__ == '__main__':
    charge = Recharge()
    charge.recharhge()
    # charge.invalid()
