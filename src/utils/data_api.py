#coding=utf-8
import io
import traceback
import json
import math
import pandas
import configparser
import logging
from logging import handlers
import os
import sys
from utils.local_config import logger
from utils.local_config import feaconf

from fdm_utils.common             import get_tb_info
from fdm_utils.common             import debug_line


CURRENT_DIR     = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR        = os.path.join(CURRENT_DIR, '../../')
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## 函数部分
## get_basic_data           获取基础数据[basic]
## get_app_data             获取app数据[app]
## get_sms_data             获取短信数据[sms]
## get_credit_time          获取授信时间
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def get_basic_data(_key="user_id",_value=None,_end_time=None):
    msg  = "success"    ##程序正常时返回success，否则返回错误信息；
    flag = 0            ##程序正常时返回0，否则返回-1；
    dst  = None         ##程序正常时返回结果，否则返回None；

    try:
        path_basic  = os.path.join(ROOT_DIR,"data/basic.csv") 
        data_df     = pandas.read_csv(path_basic)
        dst         = data_df[data_df[_key] == _value]
        logger.info("%s=%s,get_basic_data完成" % (_key,_value))
    except:
        logger.error("%s=%s,get_basic_data失败" % (_key,_value))
        msg  = get_tb_info()
        flag = -1
        dst  = None
    return msg,flag,dst


def get_app_data(_key="user_id",_value=None,_end_time=None):
    msg  = "success"    ##程序正常时返回success，否则返回错误信息；
    flag = 0            ##程序正常时返回0，否则返回-1；
    dst  = None         ##程序正常时返回结果，否则返回None；
    
    try:
        path_app = os.path.join(ROOT_DIR,"data/app.csv") 
        data_df  = pandas.read_csv(path_app)
        dst      = data_df[data_df[_key] == _value]
        logger.info("%s=%s,get_app_data完成" % (_key,_value))
    except:
        logger.error("%s=%s,get_app_data失败" % (_key,_value))
        msg  = get_tb_info()
        flag = -1
        dst  = None
    return msg,flag,dst


def get_sms_data(_key="user_id",_value=None,_end_time=None):
    msg  = "success"    ##程序正常时返回success，否则返回错误信息；
    flag = 0            ##程序正常时返回0，否则返回-1；
    dst  = None         ##程序正常时返回结果，否则返回None；

    try:
        path_sms = os.path.join(ROOT_DIR,"data/sms.csv") 
        data_df  = pandas.read_csv(path_sms)
        dst      = data_df[data_df[_key] == _value]
        logger.info("%s=%s,get_sms_data完成" % (_key,_value))
    except:
        logger.error("%s=%s,get_sms_data失败" % (_key,_value))
        msg  = get_tb_info()
        flag = -1
        dst  = None
    return msg,flag,dst

def get_credit_time(_key="user_id",_value=None):
    msg  = "success"    ##程序正常时返回success，否则返回错误信息；
    flag = 0            ##程序正常时返回0，否则返回-1；
    dst  = None         ##程序正常时返回结果，否则返回None；
    con  = Connect_db()

    if True:
        print("enter get_credit_time::")
        print("读取本地文件的尚未完成","unfix")
    try:
        dst  = con.con_mysql("dbaaa", "select credit_time from tableaaa where id = (%s)" % _value)
        dst  = int(dst.iloc[0]["credit_time"])
        logger.info("%s=%s,get_credit_time完成" % (_key,_value))
    except:
        logger.error("%s=%s,get_credit_time失败" % (_key,_value))
        msg  = get_tb_info()
        flag = -1
        dst  = None
    return msg,flag,dst


