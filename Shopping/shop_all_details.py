#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: tb_address.py
@time: 2020/9/16 9:32
@desc:
"""
# coding=utf-8

import sys
print(sys.path)

import base64
import os
import random
import sys
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # 等待浏览器加载数据
import importlib

from Shopping import ocr
from Shopping.data_base import DataBase

importlib.reload(sys)

import re
import requests
from lxml import etree

class TaoBao:
    def __init__(self, platform, good_name, task_id):
        self.data_num = 0
        self.task_id = task_id
        self.platform = platform
        self.good_name = good_name
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options = webdriver.ChromeOptions()
        # 代理ip地址
        # ip = 'http://182.87.39.42:9000'
        # options.add_argument(('--proxy-server=' + ip))
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 不加载图片,加快访问速度
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # ，获取浏览器的驱动，这里需要提前给chrome指定环境变量，如果没有指定则需要指定路径
        self.driver = webdriver.Chrome(chrome_options=options)
        # 去除 window.navigator.webdriver
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        # 窗口最大化
        self.driver.maximize_window()
        # 打开登录页面
        self.wait = WebDriverWait(self.driver, 20)  # 超时时长为20s
        self.driver.get(
            'https://login.taobao.com/member/login.jhtml?')
#         cookies = [
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1632242494.087434,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "_cc_",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "URm48syIZQ%3D%3D",
#                 "id": 1
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "_l_g_",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "Ug%3D%3D",
#                 "id": 2
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1601279157.904658,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "_m_h5_tk",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "f72e9f3eae43b198be2c66088193f525_1600681559040",
#                 "id": 3
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1601279157.904701,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "_m_h5_tk_enc",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "d52cafb57f6c3ae6a86b4498751ec202",
#                 "id": 4
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "_nk_",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "%5Cu600E%5Cu4E48%5Cu4F1A%5Cu4E28%5Cu8FD9%5Cu6837",
#                 "id": 5
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "_samesite_flag_",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "True",
#                 "id": 6
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "_tb_token_",
#                 "path": "/",
#
#                 "secure": False,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "ee3017843513a",
#                 "id": 7
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 2231397684,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "cna",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "LBaDF7fMtlkCAWVQzVmZadAL",
#                 "id": 8
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "cookie1",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "VWn7gV61f75iDWSjflg3ULQvy3nlJdnn%2FpOuD1TGhs8%3D",
#                 "id": 9
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "cookie17",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "UUphwoXyVI7o6nVyTQ%3D%3D",
#                 "id": 10
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "cookie2",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "167c6824699e79fbe0dc571449406c03",
#                 "id": 11
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "csg",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "b00bed02",
#                 "id": 12
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "dnk",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "%5Cu600E%5Cu4E48%5Cu4F1A%5Cu4E28%5Cu8FD9%5Cu6837",
#                 "id": 13
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1916037694.829795,
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "enc",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "Qpv6cUI4zCHXImZm6MN0w2ImRinNfsmAzpeAoGMIveNZM%2BoQE%2FKD%2BeNSlbBZLIAxzBOMYcPmWZ%2Be8dPmcx3umk6sSJyXdcrddjmiqmcGT%2BA%3D",
#                 "id": 14
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "existShop",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "MTYwMDY3NzY5NQ%3D%3D",
#                 "id": 15
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1632242483.799528,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "hng",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "CN%7Czh-CN%7CCNY%7C156",
#                 "id": 16
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1616229828,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "isg",
#                 "path": "/",
#
#                 "secure": False,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "BO7uM0uuPbGT5UmjZFnEwoqQP0Sw77LplKkmcxi3WPGs-45VgHvp-ZD5t2cXJ6oB",
#                 "id": 17
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1616229832,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "l",
#                 "path": "/",
#
#                 "secure": False,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "eBSNAONVOE6zAYUkBOfanurza77OSIRYYuPzaNbMiOCPOkCB5BvNWZrtt7T6C3GVh6WeR3oIr-vXBeYBqQAonxvtIosM_Ckmn",
#                 "id": 18
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1603298494.087271,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "lgc",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "%5Cu600E%5Cu4E48%5Cu4F1A%5Cu4E28%5Cu8FD9%5Cu6837",
#                 "id": 19
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1601311294.950045,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "mt",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "ci=0_1",
#                 "id": 20
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "sg",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "%E6%A0%B739",
#                 "id": 21
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1632242494.087314,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "sgcookie",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "E100kUGTXxnnjlKThnLhXsPmbFeSKvqkLdRIhOu4Ris5LBOelPCKom%2FUskPk%2FDZodbsWXSllI1Sb6B%2F8MyhH3oZFdw%3D%3D",
#                 "id": 22
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "skt",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "a0376aa52e0491d7",
#                 "id": 23
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1608482494.087284,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "t",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "dc3d2ce6daccc873fa4f8b0953e5cb9b",
#                 "id": 24
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1616229832,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "tfstk",
#                 "path": "/",
#
#                 "secure": False,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "cNOGBbAa3dW1IkXHFf16PDwBXAlRwMHVfBADTB08o9tU651cKJyrCP3VXhAYh",
#                 "id": 25
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1627001770,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "thw",
#                 "path": "/",
#
#                 "secure": False,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "cn",
#                 "id": 26
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1632242494.0874,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "tracknick",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "%5Cu600E%5Cu4E48%5Cu4F1A%5Cu4E28%5Cu8FD9%5Cu6837",
#                 "id": 27
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "uc1",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "existShop=False&cookie14=Uoe0bU5TpnxReg%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&pas=0&cookie21=VT5L2FSpdiBh",
#                 "id": 28
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1603298494.087244,
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "uc3",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "vt3=F8dCufeKwhcCDNHdOlk%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&nk2=tyM2bKZgARANlk5z&id2=UUphwoXyVI7o6nVyTQ%3D%3D",
#                 "id": 29
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1603298494.087376,
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "uc4",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "id4=0%40U2grGR1h8Ce6zDnju6usysSsHJnJcSx%2B&nk4=0%40tVBKsEDQQcxe99wVsKTE3tZ9f%2FazK3g%3D",
#                 "id": 30
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1612143070,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "UM_distinctid",
#                 "path": "/",
#
#                 "secure": False,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "173b1f1a6a418d-05bec1c05e6b95-b7a1334-149c48-173b1f1a6a5bc4",
#                 "id": 31
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": True,
#                 "name": "unb",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "2208255214253",
#                 "id": 32
#             },
#             {
#                 "domain": ".taobao.com",
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "v",
#                 "path": "/",
#
#                 "secure": False,
#                 "session": True,
#                 "storeId": "0",
#                 "value": "0",
#                 "id": 33
#             },
#             {
#                 "domain": ".taobao.com",
#                 "expirationDate": 1600736343,
#                 "hostOnly": False,
#                 "httpOnly": False,
#                 "name": "xlly_s",
#                 "path": "/",
#
#                 "secure": True,
#                 "session": False,
#                 "storeId": "0",
#                 "value": "1",
#                 "id": 34
#             }
# ]
#
#         for cookie in cookies:
#             self.driver.add_cookie(cookie)


    # 判断元素是否存在
    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag

        except Exception as e:
            print('识别失败')
            flag = False
            return flag

    def searchgood(self):
        self.driver.get('https://www.taobao.com/')
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[2]/div[3]/div/input').send_keys(
            self.good_name)  # 找出搜索框并输入搜索名称
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[2]/div[3]/div/input').send_keys(Keys.ENTER)
        self.get_infos()

    # 模拟向下滑动
    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            js = "var q = document.documentElement.scrollTop=" + str(300 + 200 * i)
            self.driver.execute_script(js)  # 使用js代码模拟滑动
            time.sleep(0.1)
        time.sleep(0.2)

    # 模拟翻页操作
    def next_page(self, page_number):
        print(f'=================================正在爬取淘宝{0}---第{page_number}页数据=================================')
        time.sleep(0.5)
        try:
            # if page_number <= 4:  # 1-4页
            #     # '//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a'
            #     next_button = self.driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a')
            # elif 5 <= page_number <= 6:  # 5-6页
            #     next_button = self.driver.find_element_by_xpath(
            #         '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/ul/li[{}]/a'.format(4 + page_number))
            # elif int(self.total_page) - 1 <= page_number <= int(self.total_page):  # 最后倒数两页
            #     next_button = self.driver.find_element_by_xpath(
            #         '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/ul/li[10]/a')
            # else:  # 剩余页数
            next_button = self.driver.find_element_by_xpath(
                    '//*[@class="form"]/span[3]')
            # 获取页码输入框
            next_input = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[2]/input')
            # 将当前输入框中的内容清空，并重置为page_number
            next_input.clear()
            next_input.send_keys(page_number)
    
            time.sleep(1.8)
            next_button.click()
        except:
            print('页码问题，请仔细核对！')

    def login2(self):  # 手动扫码登录
        time.sleep(13)
        
    # 得到所有的页数
    def get_total_page(self):
        time.sleep(5.4)
        # 先等待所有的商品都加载完/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[1]
        page_total = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[1]').text
        print(page_total)
        result = page_total.strip("共 ").replace(' 页，', '')
        return result

    # 得到商品集
    def get_infos(self):
        self.total_page = self.get_total_page()
        
        for i in range(4, int(self.total_page) + 1):
            # 等待页面商品数据加载完成
            time.sleep(2.6)
            # 模拟向下滑动
            self.swipe_down(2)
            try:
                # 获取本页面源代码
                html = self.driver.page_source
                # print html
                s = etree.HTML(html)
                tds = s.xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div[21]/div/div/div[1]/div/div[2]')
                goods_data = [] # 存放每一个td的的数据
                for td in tds:
                    manager = td.xpath('./div[3]/div[1]/a/span[2]/text()')  # 掌柜名
                    manager_href = td.xpath('./div[3]/div[1]/a/@href')  # 店铺连接
                    name = td.xpath('./div[2]/a')  # 商品名
                    
                    price = td.xpath('./div[1]/div[1]/strong/text()')  # 价格
                    href = td.xpath('./div[2]/a/@href')  # 商品链接
                    icon = td.xpath('./div[4]/div[1]/ul/li/a/span/@class')  # 天猫标志

                    manager = manager[0] if len(manager) > 0 else ''
                    manager_href = manager_href[0] if len(manager_href) > 0 else ''
                    if manager_href.find('http') == -1:
                        manager_href = 'https:' + manager_href
                    name = name[0].xpath('string(.)') if len(name) > 0 else ''
                    name = name.replace(' ', '').replace("\n", "").replace("\r", "")
                    price = price[0] if len(price) > 0 else ''
                    href = href[0] if len(href) > 0 else ''
                    if href.find('http') == -1:
                        href = 'https:' + href
                    icon = icon[0] if len(icon) > 0 else ''

                    weight = ''
                    price_item = ''
                    Co_name = ''
                    reg_address = ''
                    
                    if icon == "icon-service-tianmao":  # 如果是天猫店铺
                        self.driver.get(href)
                        
                        time.sleep(2)
                        html = self.driver.page_source  # 进入天猫店铺
                        s = etree.HTML(html)
                        

                        try:
                            logo = s.xpath('//*[@id="mallLogo"]/span/a/@href')  # 判断天猫类型
                            logo = logo[0] if len(logo) > 0 else '0'
                            # 处理天猫超市
                            if logo == "//chaoshi.tmall.com?notjump=True&_ig=logo":
                                # 重量
                                weight = s.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[3]/dl[2]/dd/em/text()')
                                weight = weight[0] if len(weight) > 0 else '0'
                                weight = (float(weight) * 1000)
                                price_item = 0

                            # 处理除天猫超市的天猫店铺
                            else:
                                weight = s.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[3]/dl[2]/dd/text()')
                                weight = weight[0] if len(weight) > 0 else '0'
                                weight = weight.replace('g', '')

                                price_item = s.xpath('//*[@id="J_StrPriceModBox"]/dd/span[2]/text()')  # 价格/重量
                                price_item = price_item[0] if len(price_item) > 0 else ''

                                img_name = manager + '.png'  # 天猫图片取名字
                                # 调用数据库判断天猫company具体信息是否已经存在
                                sql_exist = f'''
                                          select NAME,ADDRESS from "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY" where SHOP ='{manager}'
                                '''
                                sql_exist_data = db.select_tb(sql_exist)
                                if len(sql_exist_data) <= 0:
                                    # 若不存在公司信息
                                    co_href = re.findall(r'href="(.*?)" class="tm-gsLink"', html, re.I)  # 公司资质链接
                                    co_href = co_href[0] if len(co_href) > 0 else ''
                                    co_href = co_href.replace("u'", '').replace("'", '')
                                    self.driver.get('https:' + co_href)  # 进入公司资质链接
                                    
                                    time.sleep(1)
                                    flag = True
                                    while flag:  # 若flag为真，验证码匹配失败，则验证码重新输入
                                        try:
                                            # img_href = s.xpath('//*[@id="J_CheckCode"]/@data-url')  # 验证码链接
                                            # img_href = img_href[0] if len(img_href) > 0 else ''
                                            # headers = {
                                            #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
                                            #
                                            # response = requests.get(url='http:' + img_href, headers=headers)  # 请求验证码链接
                                            # img_data = response.content  # 读取验证码数据
                                            # with open('yzm.jpg', mode='wb') as f:  # 写入验证码
                                            #     f.write(img_data)
                                            # code = ocr.baidu('yzm.jpg')  # 调用接口识别验证码
                                            code = '9GNN'
                                            self.driver.find_element_by_xpath(
                                                '/html/body/div/div/div/div[1]/form/input[2]').clear()  # 清除输入框
                                            self.driver.find_element_by_xpath(
                                                '/html/body/div/div/div/div[1]/form/input[2]').send_keys(code)  # 输入验证码
                                            self.driver.find_element_by_xpath(
                                                '/html/body/div/div/div/div[1]/form/input[2]').send_keys(Keys.ENTER)
                                            time.sleep(0.38)
                                            html_flag = self.driver.page_source  # 获取网页源码
                                            s_flag = etree.HTML(html_flag)
                                            # 判断是否存在“确定”按钮
                                            button = s_flag.xpath(
                                                '//*[@id="J_LicenceCheckPop"]/div/div/div[1]/form/div[1]/button/text()')
                                            if len(button) > 0:
                                                flag = True
                                                self.driver.back()  # 每错误一次回退到页面
                                            else:
                                                flag = False

                                        except Exception as e:
                                            print('天猫验证码出错', e)
                                    img_src = s_flag.xpath('/html/body/div/div[2]/div/img/@src')  # 返回企业加密信息
                                    img_src = img_src[0] if len(img_src) > 0 else ''
                                    img_src = img_src.replace('data:image/png;base64,', '')  # 去除头部不需要信息
                                    img_src_data = base64.b64decode(img_src)  # 对企业信息进行解密

                                    with open('CoLicense' + '/' + img_name, 'wb') as f:  # 写入图片
                                        f.write(img_src_data)
                                    self.driver.back()  # 回到验证码

                                    self.driver.back()  # 回到店铺
                                    tianmao_company_data = ocr.get_tencent_reg('CoLicense' + '/' + img_name)
                                    str_list = ','.join(tianmao_company_data)
                                    
                                    tm_name = re.findall("名.{0,4}称:([^,]*)", str_list)
                                    tm_name = tm_name[0] if len(tm_name) > 0 else ''
                                    tm_name = tm_name.replace(']', '')
                                    address = re.findall("住.{0,4}所:([^,]*)", str_list)
                                    address = address[0] if len(address) > 0 else ''
                                    # print(tm_name, address)
                                    # 调用sql将数据插入数据库
                                    values = [(str(manager), str(tm_name), str(address))]
                                    sql_tb = """
                                                insert into "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY"
                                                ("SHOP", "NAME", "ADDRESS") VALUES(?,?,?);
                                                """
                                    db.insert_tb(sql_tb, values)
                                    sql_tb = f'''
                                            select NAME,ADDRESS from "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY" where SHOP ='{manager}'
                                    '''
                                    sql_exist_data = db.select_tb(sql_tb)
                                Co_name = sql_exist_data[0][0]
                                reg_address = sql_exist_data[0][1]
                                
                        except Exception as e:
                            print('天猫weight出错', e)

                        self.driver.back()  # 回到搜索店铺
                    else:  # 淘宝店铺  ‘//scportal.taobao.com/quali_show.htm?uid=2207759828325&qualitype=1’
                        if href.find('http') == -1:
                            href = 'https:' + href
                        self.driver.get(href)  # 进入店铺详情
                        time.sleep(2)
                        html = self.driver.page_source
                        s = etree.HTML(html)
                        
                        try:
                            weight = s.xpath('//*[@id="detail"]/div[1]/div[1]/div/div[2]/div/div/ul/li[2]/text()')
                            weight = weight[1] if len(weight) > 0 else ''
                            weight = weight.replace(' ', '').replace('g', '').replace("\n", "")
                            
                            price_item = s.xpath('//*[@id="J_StrPriceModBox"]/div/span/text()')
                            price_item = price_item[0] if len(price_item) > 0 else ''
                            
                            # 店铺名称
                            manager = s.xpath('//*[@id="J_ShopInfo"]/div/div[1]/div[1]/dl/dd/strong/a/@title')
                            if len(manager) > 0:
                                manager = manager[0]
                            else:
                                manager = s.xpath('//*[@id="header-content"]/div[2]/div[3]/div[1]/p/span[2]/@title')
                                manager = manager[0] if len(manager) > 0 else ''
                            manager = manager.replace('\t', '').replace(' ', '').replace('\n', '').replace('\r', '')
                        except Exception as e:
                            print("淘宝weight出错", e)

                        shopInfo = s.xpath('//*[@id="J_ShopInfo"]/div[1]/div[1]/div[5]/dl/dd/a[1]/@class')
                        shopInfo = shopInfo[0] if len(shopInfo) > 0 else ''  # 判断是否支付宝个人认证
                        # 调用数据库判断淘宝company具体信息是否已经存在
                        sql_exist = f'''
                                select NAME,ADDRESS from "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY" where SHOP ='{manager}'
                        '''
                        sql_exist_data = db.select_tb(sql_exist)
                        if len(sql_exist_data) <= 0:
                            if (shopInfo == 'tb-icon tb-icon-alipay-persion-auth'):  # 若是个人店铺
                                shipIcon = s.xpath('//*[@class="tb-icon tb-icon-qualification"]/@href') #检测经营许可证图标
                                shipIcon = shipIcon[0] if len(shipIcon) > 0 else ''
                                if shipIcon != '':
                                    self.driver.get(shipIcon)  # 进入店铺验证码环节
                                    time.sleep(1)
                                    while True:
                                        try:
                                            action = ActionChains(self.driver)
                                            source = self.driver.find_element_by_xpath(
                                                "/html/body/div/form/div/div/div[1]/span")  # 需要滑动的元素
                                            action.click_and_hold(source).perform()  # 鼠标左键按下不放
                                            time.sleep(0.5)
                                            action.move_by_offset(470, 0)  # 需要滑动的坐标
                                            time.sleep(0.02)
                                            action.release().perform()  # 释放鼠标
                                            time.sleep(1)
                                            break
                                        except:
                                            time.sleep(30)
        
                                    flag = True
                                    while flag:  # 若flag为真，验证码匹配失败，则验证码重新输入
                                        try:
                                            # 获取验证码
                                            # code_href = self.driver.find_element_by_xpath(
                                            #     '//*[@id="nc_1__imgCaptcha_img"]/img') \
                                            #     .get_attribute('src')
                                            # code_href = code_href.replace('data:image/jpg;base64,', '')  # 去除头部不需要信息
                                            # decode_data = base64.b64decode(code_href)  # 将base64解码
                                            # with open('VfCode\\yzm.jpg', 'wb') as im_f:
                                            #     im_f.write(decode_data)
                                            # Tcode = ocr.baidu('VfCode\\yzm.jpg')  # 调用接口识别验证码
                                            Tcode = 'USN8'
                                            self.driver.find_element_by_xpath(
                                                '//*[@id="nc_1_captcha_input"]').clear()  # 清除输入框
                                            self.driver.find_element_by_xpath(
                                                '//*[@id="nc_1_captcha_input"]').send_keys(
                                                Tcode)  # 输入验证码
                                            self.driver.find_element_by_xpath(
                                                '//*[@id="nc_1_captcha_input"]').send_keys(Keys.ENTER)
                                            self.wait = WebDriverWait(self.driver, 10)  # 超时时长为20s
                                            time.sleep(0.38)
                                            checkcode_html = self.driver.page_source  # 获取网页源码
                                            checkcode_s = etree.HTML(checkcode_html)
                                            self.wait = WebDriverWait(self.driver, 10)  # 超时时长为20s
                                            # # 判断是否存在checkcode
                                            checkcode = checkcode_s.xpath('//*[@id="formId"]/@class')
                                            if len(checkcode) > 0:
                                                flag = True
                                            else:
                                                flag = False
                                                
                                        except Exception as e:
                                            print('淘宝验证码出错', e)
                                    Tcode_html = self.driver.page_source  # 获取网页源码
                                    time.sleep(0.4)
                                    Tcode_res = etree.HTML(Tcode_html)
                                    picture1 = Tcode_res.xpath('//*[@id="licenses-gallery"]/div/a[1]/img/@src')
                                    picture1 = 'https:' + picture1[0] if len(picture1) > 0 else ''
                                    picture1_data = requests.get(picture1)
                                    img_name = manager + '.jpg'  # 淘宝个人店铺图片取名字
                                    with open('CoLicense' + '/' + img_name, 'wb') as pf:
                                        pf.write(picture1_data.content)
                                    self.driver.back()  # 回到滑块验证
                                    self.driver.back()  # 回到店铺
                                    tb_coname, tb_address = ocr.get_tencent_biz('CoLicense' + '/' + img_name)
                                    # 调用sql将数据插入数据库
                                    values = [(str(manager), str(tb_coname), str(tb_address))]
                                    sql_tb = """
                                            insert into "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY"
                                            ("SHOP", "NAME", "ADDRESS") VALUES(?,?,?);
                                     """
                                    db.insert_tb(sql_tb, values)
    
                            else:   # 淘宝企业店铺
                                # 找到淘宝企业店铺的'工商执照'对应的href
                                shipIcon = s.xpath('//*[@id="header-content"]/div[2]/div[3]/div[2]/div[1]/p[5]/a[1]/@href')
                                shipIcon = shipIcon[0] if len(shipIcon) > 0 else ''
                                if shipIcon != '':
                                    self.driver.get(shipIcon)  # 进入店铺验证码环节
                                    time.sleep(1)
                                    
                                    while True:
                                        try:
                                            action = ActionChains(self.driver)
                                            source = self.driver.find_element_by_xpath(
                                                "/html/body/div/form/div/div/div[1]/span")  # 需要滑动的元素
                                            action.click_and_hold(source).perform()  # 鼠标左键按下不放
                                            time.sleep(0.5)
                                            action.move_by_offset(470, 0)  # 需要滑动的坐标
                                            time.sleep(0.02)
                                            action.release().perform()  # 释放鼠标
                                            time.sleep(1)
                                            break
                                        except:
                                            time.sleep(30)
    
                                    flag = True
                                    while flag:  # 若flag为真，验证码匹配失败，则验证码重新输入
                                        try:
                                            # 获取验证码
                                            # code_href = self.driver.find_element_by_xpath('//*[@id="nc_1__imgCaptcha_img"]/img')\
                                            #     .get_attribute('src')
                                            # code_href = code_href.replace('data:image/jpg;base64,', '') # 去除头部不需要信息
                                            # decode_data = base64.b64decode(code_href)  # 将base64解码
                                            # with open('VfCode\\yzm.jpg', 'wb') as im_f:
                                            #     im_f.write(decode_data)
                                            # Tcode = ocr.baidu('VfCode\\yzm.jpg')   # 调用接口识别验证码
                                            Tcode = 'USN8'
                                            self.driver.find_element_by_xpath('//*[@id="nc_1_captcha_input"]').clear()  # 清除输入框
                                            self.driver.find_element_by_xpath('//*[@id="nc_1_captcha_input"]').send_keys(
                                                Tcode)  # 输入验证码
                                            self.driver.find_element_by_xpath('//*[@id="nc_1_captcha_input"]').send_keys(Keys.ENTER)
                                            self.wait = WebDriverWait(self.driver, 10)  # 超时时长为20s
                                            time.sleep(0.38)
                                            checkcode_html = self.driver.page_source  # 获取网页源码
                                            checkcode_s = etree.HTML(checkcode_html)
                                            self.wait = WebDriverWait(self.driver, 10)  # 超时时长为20s
                                            # 判断是否存在checkcode
                                            checkcode = checkcode_s.xpath('//*[@id="formId"]/@class')
                                            if len(checkcode) > 0:
                                                flag = True
    
                                            else:
                                                flag = False
                                                
                                        except Exception as e:
                                            print('淘宝验证码出错', e)
                                    Tcode_html = self.driver.page_source  # 获取网页源码
                                    time.sleep(0.38)
                                    Tcode_res = etree.HTML(Tcode_html)
    
                                    tb_coname = Tcode_res.xpath('//*[@id="index"]/div[1]/div[2]/text()')
                                    tb_coname = tb_coname[0] if len(tb_coname) > 0 else ''
                                    tb_address = Tcode_res.xpath('//*[@id="index"]/div[3]/div[2]/text()')
                                    tb_address = tb_address[0] if len(tb_address) > 0 else ''
                                    self.driver.back()  # 回到滑块验证
                                    self.driver.back()  # 回到店铺
                                    Co_name = tb_coname
                                    reg_address = tb_address
                                    # 调用sql将数据插入数据库
                                    values = [(str(manager), str(tb_coname), str(tb_address))]
                                    sql_tb = """
                                            insert into "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY"
                                            ("SHOP", "NAME", "ADDRESS") VALUES(?,?,?);
                                     """
                                    db.insert_tb(sql_tb, values)
                        else:
                            Co_name = sql_exist_data[0][0]
                            reg_address = sql_exist_data[0][1]
                        
                        self.driver.back()  # 回到搜索店铺

                    print(self.platform, manager, manager_href, name, href, price,
                              weight, price_item, Co_name, reg_address)
                    get_date = time.strftime('%Y-%m-%d %H:%M:%S')
                    # 将每次数据存入一个元组
                    value = [(self.platform, manager, manager_href, name, href, str(price),
                              str(weight), price_item, Co_name, reg_address, str(get_date), self.task_id)]
                    goods_data.append(value)
                    self.data_num += 1
                    
                    # 每次插入一个数据
                    sql_tb = '''
                        insert into "TENCENTAPI"."PD_SPIDER_SHOPS"(platform, shop, shop_url, name, name_url,
                        price_rmb, weight, unit_price, company_name, company_address, get_date, task_id)
                         VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
                    '''
                    db.insert_tb(sql_tb, value)
            except Exception as e:
                print('出错', e)
            finally:
               pass

            time.sleep(2)
            # 下一页
            if i < int(self.total_page):
                self.next_page(i + 1)
        
        # 程序结束，关闭浏览器
        self.driver.quit()


class JingDong:
    def __init__(self, platform, good_name, task_id):
        self.data_num = 0
        self.task_id = task_id
        self.platform = platform
        self.good_name = good_name
        print('京东爬虫准备就绪!')
    
    def getHTMLText(self, url):
        f_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        }
        
        try:
            r = requests.get(url=url, headers=f_headers)
            r.raise_for_status()  # 判断返回的Response类型状态是不是200。如果是200，返回的内容是正确的，不是200，他就会产生一个HttpError的异常
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ""
    
    def get_name_address(self, shop_num):
        shop_license = 'https://mall.jd.com/showLicence-{}.html'.format(shop_num)
        pic_url = 'https://mall.jd.com/sys/vc/createVerifyCode.html?random=0.136654166303658'
        session = requests.session()
        flag = 0    # 设置100次不出结果就退出，防止死循环
        while True:
            flag += 1
            response = session.get(url=pic_url, verify=False)
    
            with open('VfCode\\jd_yzm.jpg', 'wb') as f:
                f.write(response.content)
    
            code = ocr.baidu('VfCode\\jd_yzm.jpg')
            
            data = {
                'verifyCode': code,
            }
            html = session.post(url=shop_license, data=data)
            name = re.findall('<label class="jLabel">企业名称.*?</label>[\s]*?<span>(.*?)</span>', html.text)
            address = re.findall('<label class="jLabel">公司地址.*?</label>[\s]*?<span>(.*?)</span>', html.text)
            if len(name) > 0 and len(address) > 0:
                return name[0], address[0]
            else:
                if flag >= 100:
                    return [], []
                    
                pass

    
    def sql_exist(self, shop_name):
        # 调用数据库判断company具体信息是否已经存在
        sql_exist = f'''
                   select NAME,ADDRESS from "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY" where SHOP ='{shop_name}'
           '''
        sql_exist_data = db.select_tb(sql_exist)
        if len(sql_exist_data) > 0:
            return sql_exist_data
        else:
            return []
            
    def parsePage(self, html):
        try:
            tds = html.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/div/li/div')
            
            for td in tds:
                
                shop_name = td.xpath('./div[5]/span/a/@title')
                shop_name = shop_name[0] if len(shop_name) > 0 else ''
                shop_href = td.xpath('./div[5]/span/a/@href')
                shop_href = 'https:' + shop_href[0] if len(shop_href) > 0 else ''
                good_name = td.xpath('./div[3]/a/em')
                good_name = good_name[0].xpath('string(.)') if len(good_name) > 0 else ''
                good_name = good_name.replace(' ', '').replace("\n", "").replace("\r", "")
                good_href = td.xpath('./div[3]/a/@href')
                good_href = 'https:' + good_href[0] if len(good_href) > 0 else ''
                price = td.xpath('./div[2]/strong/i/text()')
                price = price[0] if len(price) > 0 else ''
                good_html = self.getHTMLText(good_href)
                weight = re.findall('商品毛重：(.*?)</li>', good_html)  # <dt>净含量</dt><dd>(.*?)</dd>
                if len(weight) > 0:
                    weight = weight[0]
                else:
                    weight = re.findall('<dt>净含量</dt><dd>(.*?)</dd>', good_html)
                    weight = weight[0] if len(weight) > 0 else 1
                
                if weight.find('kg') == -1:  # 没找到
                    unit = float(weight.replace('kg', '').replace('g', ''))
                else:
                    unit = float(weight.replace('kg', '').replace('g', '')) * 1000  # kg-->g
                unit_price = float(price) / (unit / 500)
                unit_price = round(unit_price, 2)  # 保留两位小数
                Co_name = ''
                reg_address = ''
                # 对店铺公司名称和地址的判断
                sql_exist_data = self.sql_exist(shop_name)
                if len(sql_exist_data) > 0:
                    Co_name = sql_exist_data[0][0]
                    reg_address = sql_exist_data[0][1]
                else:
                    shop_num = re.findall('-([\d]+).', shop_href)
                    if len(shop_num) > 0:
                        shop_num = shop_num[0]
                        Co_name, reg_address = self.get_name_address(shop_num)
                        # 调用sql将数据插入数据库
                        values = [(str(shop_name), str(Co_name), str(reg_address))]
                        sql_tb = """
                                   insert into "TENCENTAPI"."PD_SPIDER_SHOP_COMPANY"
                                   ("SHOP", "NAME", "ADDRESS") VALUES(?,?,?);
                            """
                        db.insert_tb(sql_tb, values)
                        
                print(self.platform, shop_name, shop_href, good_name, good_href, price,
                      weight, unit_price, Co_name, reg_address)
                get_date = time.strftime('%Y-%m-%d %H:%M:%S')
                # 将每次数据存入一个元组
                value = [(self.platform, shop_name, shop_href, good_name, good_href, str(price),
                      str(weight), str(unit_price), Co_name, reg_address, str(get_date), self.task_id)]
                self.data_num += 1

                # 每次插入一个数据
                sql_tb = '''
                       insert into "TENCENTAPI"."PD_SPIDER_SHOPS"(platform, shop, shop_url, name, name_url,
                       price_rmb, weight, unit_price, company_name, company_address, get_date, task_id)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
                   '''
                db.insert_tb(sql_tb, value)
                
        except:
            print("京东爬取商品数据错误！")
    
    def search(self):
        goods = self.good_name  # 商品名称
        start_url = 'https://search.jd.com/Search?keyword={}'.format(goods)
        start_html = self.getHTMLText(start_url)
        depth = int(re.findall('page_count:"([0-9]*)"', start_html)[0])
        for i in range(1, depth + 1):
            try:
                print('=================================正在爬取京东{0}---第{1}页数据================================='.format(
                    goods, i))
                url = 'https://search.jd.com/Search?keyword={0}&page={1}&scrolling=y'.format(
                    goods, i)
                html = self.getHTMLText(url)
                # print(html)
                html = etree.HTML(html)
                self.parsePage(html)
            except:
                continue

if __name__ == '__main__':
    db = DataBase()
    # 从数据库中查找未爬取购物网站的平台名称, 物品名称任务ID
    sql = """
    select WEB_NAME, SPIDER_OBJECT, ID
    from "TENCENTAPI"."PD_SPIDER_TASK" where (WEB_SORT = '购物网站')and FLAG = 0
    """
    result = db.select_tb(sql)
    print(result, len(result))
    for i in range(len(result)):
        if result[i][0] == '淘宝':  # 淘宝
            start_time = str(time.strftime('%Y-%m-%d %H:%M:%S'))
            tb = TaoBao(result[i][0], result[i][1], result[i][2])
            # tb.login2()
            # tb.searchgood()
            end_time = str(time.strftime('%Y-%m-%d %H:%M:%S'))
            sql_update = """
    		        update "TENCENTAPI"."PD_SPIDER_TASK" set FLAG = 1, DATA_NUM = {0},START_TIME = '{1}', END_TIME = '{2}' where ID = {3}
    		""".format(tb.data_num, start_time, end_time, result[i][2])
            db.update(sql_update)
        else:  # 京东
            start_time = str(time.strftime('%Y-%m-%d %H:%M:%S'))
            jd = JingDong(result[i][0], result[i][1], result[i][2])
            jd.search()
            end_time = str(time.strftime('%Y-%m-%d %H:%M:%S'))
            sql_update = """
                    update "TENCENTAPI"."PD_SPIDER_TASK" set FLAG = 1, DATA_NUM = {0},START_TIME = '{1}', END_TIME = '{2}' where ID = {3}
            """.format(jd.data_num, start_time, end_time, result[i][2])

            db.update(sql_update)

    
