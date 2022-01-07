#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !@Author: 练素琼
# !Email: lsqiong_1@histudy.com
# !Date: 2020-11-03 9:25

import re
from selene import browser
# from common.commonmethod import bw
import time
from selenium.webdriver.chrome import webdriver
from histudy import log
from selenium import webdriver as wb


def is_element_exist(driver, element):
    flag = True
    try:
        driver.find_element_by_xpath(element)
        return flag
    except:
        flag = False
        return flag



def open_mfs_wendu(student_name, creditcard, phone):
    chrome = {
        "browserName": "chrome",
        "version": "",
        "platform": "ANY",
        "enableVNC": True,
        "enableVideo": True,
        "name": "chrome",
        "chromeOptions": {
            "args": [
                "--window-size=1900,1080",
            ]
        }
    }
    driver = webdriver.RemoteWebDriver(command_executor="http://192.168.1.24:4444/wd/hub",
                                       desired_capabilities=chrome)

    url = "https://ijy.xmtaedu.cn/Wxuser/User/bind2.html"
    browser.set_driver(driver)  # 包含了登录,传入driver
    browser.driver().get(url)
    time.sleep(3)
    browser.driver().find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/div/input").send_keys(
        student_name)
    time.sleep(0.5)
    browser.driver().find_element_by_xpath("//*[@id='app']/div[3]/div[2]/div/div/input").send_keys(
        creditcard)
    time.sleep(0.5)
    browser.driver().find_element_by_xpath("//*[@id='app']/div[3]/div[3]/div/div/input").send_keys(phone)
    time.sleep(4)
    # browser.driver().get("https://ijy.xmtaedu.cn/wxuser/subao/index")
    browser.driver().find_element_by_xpath("//*[@id='app']/div[4]/button").click()
    time.sleep(2)
    browser.driver().get("https://ijy.xmtaedu.cn/wxuser/subao/index")
    #点击练王康的名字
    time.sleep(3)
    browser.driver().find_element_by_xpath("//input[@value='350824201510214611']").click()
    #点击正常
    browser.driver().find_element_by_xpath("//input[@value='0']").click()
    time.sleep(2)
    #点击提交
    browser.driver().find_element_by_xpath("//*[@id='box']/div[5]/div/div/a").click()
    time.sleep(2)
    # 点击练王娇的名字
    browser.driver().find_element_by_xpath("//input[@value='350824201402084688']").click()
    # 点击正常
    browser.driver().find_element_by_xpath("//input[@value='0']").click()
    time.sleep(3)
    # 点击提交
    browser.driver().find_element_by_xpath("//*[@id='box']/div[5]/div/div/a").click()

if __name__ == '__main__':
        open_mfs_wendu("练王娇", "350824201402084688", "19959266347")
