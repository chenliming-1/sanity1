#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2020-11-03 16:04
def getFirstPinYin(pinyin):
    listaa = []
    for item in pinyin:
        for i in item:
            print(i)
            if i.isdecimal():
                listaa.append(i)
            else:
                first = i[0:1]
                listaa.append(first)
    str1 = ''.join(listaa)
    return str1


