#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: ocr_baidu_tencent.py
@time: 2020/9/22 13:27
@desc:
"""


import base64
import time
from aip import AipOcr
import re
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


# 百度通用识字
def baidu(filePath):
    # 百度识字账号
    APP_ID = '21577308'
    API_KEY = 'GIZsgTXmtdxLAbzNUucUzUQb'
    SECRET_KEY = '0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'

    f = open(filePath, 'rb')
    image = f.read()
    options = {
        'detect_direction': 'True',
        'language_type': 'ENG',
    }
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 调用通用文字识别接口
    time.sleep(0.51)
    result = client.basicGeneral(image, options)
    # for word in result['words_result']:
    #     print word['words']
    try:
        code = result['words_result'][0]['words']
    except Exception as e:
        code = '7FKT'
    return code


# 腾讯通用识字
def get_tencent_reg(img_file_dir):
    secret_id = "AKIDXjfVfZDDySfx1OHKt63lCNIwUBhxhceR"
    secret_key = "g5LPDUVdV8XfYHju87oEOJyMTfcJkupW"
    try:
        with open(img_file_dir, 'rb') as f:
            img_data = f.read()
        img_base64 = base64.b64encode(img_data)
        params = '{"ImageBase64":"' + str(img_base64, 'utf-8') + '"}'
        
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)
        
        req = models.GeneralBasicOCRRequest()
        req.from_json_string(params)
        resp = client.GeneralBasicOCR(req).to_json_string()
        ret_list = re.findall(r'"DetectedText": "(.*?)"', resp)
        return ret_list
    
    except TencentCloudSDKException as err:
        print(err)
        return []


# 腾讯卡证文字识别
def get_tencent_biz(img_file_dir):
    secret_id = "AKIDXjfVfZDDySfx1OHKt63lCNIwUBhxhceR"
    secret_key = "g5LPDUVdV8XfYHju87oEOJyMTfcJkupW"
    try:
        with open(img_file_dir, 'rb') as f:
            img_data = f.read()
        img_base64 = base64.b64encode(img_data)
        params = '{"ImageBase64":"' + str(img_base64, 'utf-8') + '"}'
        
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)
        
        req = models.BizLicenseOCRRequest()
        req.from_json_string(params)
        resp = client.BizLicenseOCR(req)
        return resp.Name, resp.Address
    
    except TencentCloudSDKException as err:
        print(err)
        return '', ''