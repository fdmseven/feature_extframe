#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
import os
import traceback
import socket
import time
import urllib
import json
import datetime
from featureset.models  import CFeature
from utils.local_config import feaconf
from utils.local_config import logger

from fdmutils.common       import get_tb_info
from fdmutils.common       import debug_line

class CBasicFeature(CFeature):
    def __init__(self,_origin_data=None,_key=None,_value=None,_end_time=None):
        self.m_key          = _key
        self.m_value        = _value
        self.m_origin_data  = _origin_data
        self.m_feaconf       = feaconf
        self.m_end_time     = _end_time
        self.m_feature_map  = {
            ###########################
            10001000:self.basic_realname_ocrname,        ##10001000 = 真实姓名与OCR识别姓名是否一致
            10002000:self.basic_realname_thirdname,      ##10002000 = 真实姓名与第三方真实姓名是否一致
            10003000:self.basic_ocrname_thirdname,       ##10003000 = OCR识别姓名与第三方真实姓名是否一致
            10004000:self.basic_ismiddlename,            ##10004000 = 是否填写middlename
            10005000:self.basic_islastname,              ##10005000 = 是否填写lastname
            10006000:self.basic_middlename_len,          ##10007000 = middlename的长度
            10007000:self.basic_lastname_len,            ##10006000 = lastname的长度
        }
        
        pass

    def init(self):
        self.m_fid_list = self.m_feaconf['basic']
        self.m_flag     = "basic"
        pass

    ###################################
    ## 特征计算的函数
    ###################################
    def basic_realname_ocrname(self):
        self.m_origin_data['basic_realname_ocrname'] = self.m_origin_data[['realname', 'ocr_realname']].apply(lambda x: 1 if x['realname']==x['ocr_realname'] else 0, axis=1)
        dst = self.m_origin_data.iloc[0]['basic_realname_ocrname']
        if False:
            print("enter basic_realname_ocrname::")
            print(self.m_origin_data[["realname","ocr_realname"]])
        return dst

    def basic_realname_thirdname(self):
        self.m_origin_data['basic_realname_thirdname'] = self.m_origin_data[['realname', 'third_name']].apply(lambda x: 1 if x['realname']==x['third_name'] else 0, axis=1)
        dst = self.m_origin_data.iloc[0]['basic_realname_thirdname']
        if False:
            print("enter basic_realname_thirdname::")
            print(self.m_origin_data[["realname","third_name"]])
        return dst

    def basic_ocrname_thirdname(self):
        self.m_origin_data['basic_ocrname_thirdname'] = self.m_origin_data[['ocr_realname', 'third_name']].apply(lambda x: 1 if x['ocr_realname']==x['third_name'] else 0, axis=1)
        dst = self.m_origin_data.iloc[0]['basic_ocrname_thirdname']
        if False:
            print("enter basic_ocrname_thirdname::")
            print(self.m_origin_data[["ocr_realname","third_name"]])
        return dst
    
    def basic_ismiddlename(self):
        dst = 0
        if False:
            print("enter basic_ismiddlename::")
            print("\t",self.m_origin_data.iloc[0]["middle_name"])
        if self.m_origin_data.iloc[0]["middle_name"]:
            dst = 1
        else:
            dst = 0
        return dst

    def basic_islastname(self):
        dst = 0
        if False:
            print("enter basic_islastname::")
            print("\t",self.m_origin_data.iloc[0]["last_name"])
        if self.m_origin_data.iloc[0]["last_name"]:
            dst = 1
        else:
            dst = 0
        return dst

    def basic_middlename_len(self):
        dst = len(self.m_origin_data.iloc[0]["middle_name"])
        if False:
            print("enter basic_middlename_len::")
            print("\t",self.m_origin_data.iloc[0]["middle_name"])
        return dst
    
    def basic_lastname_len(self):
        dst = len(self.m_origin_data.iloc[0]["last_name"])
        if False:
            print("enter basic_lastname_len::")
            print("\t",self.m_origin_data.iloc[0]["last_name"])
        return dst

