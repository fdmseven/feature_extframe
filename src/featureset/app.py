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
from featureset.models   import CFeature
from utils.local_config  import feaconf
from utils.local_config  import logger
from utils.time_api      import time2datt
from utils.get_model_var import model_app_type_dict

from fdm_utils.common             import get_tb_info
from fdm_utils.common             import debug_line

class CAppFeature(CFeature):
    def __init__(self,_origin_data=None,_key=None,_value=None,_end_time=None):
        self.m_key          = _key
        self.m_value        = _value
        self.m_origin_data  = _origin_data
        self.m_feaconf       = feaconf
        self.m_end_time     = _end_time
        self.m_feature_map  = {
            ###########################
            40001000:self.app_count,                ##40001000 = app的数量
            40002000:self.app_update_rate,          ##40002000 = app的更新比例
            40003000:self.app_isinit_rate,          ##40003000 = 预装app的比例
            40004000:self.app_isinstall_rate,       ##40004000 = 自装app的比例
            40005000:self.app_interval_hours,       ##40005000 = 安装nanopay与授信时间的间隔小时数
            40006000:self.app_isbank_rate,          ##40006000 = 银行app的比例
            40007000:self.app_isloan_rate,          ##40007000 = 借贷app的比例
            40008000:self.app_isjingpin_rate,       ##40008000 = 竞品app的比例
            40009000:self.app_isloan_night_rate,    ##40009000 = 晚上安装借贷类app的比例
            40010000:self.app_isloan_day_rate,      ##40010001 = 白天安装借贷类app的比例
        }
        pass



    def init(self):
        self.m_fid_list = self.m_feaconf['app']
        self.m_flag     = "app"
        pass

    ###################################
    ## 特征计算的函数
    ###################################
    def app_count(self):
        dst  = self.m_origin_data.shape[0]
        return dst

    def app_update_rate(self):
        total_cnt  = self.m_origin_data.shape[0]
        update_cnt = 0
        for i in range(total_cnt):
            install_time = self.m_origin_data.iloc[i]["timestamps"]
            update_time  = self.m_origin_data.iloc[i]["last_timestamps"]
            if int(update_time) > int(install_time):
                update_cnt += 1
        return update_cnt*1.0/total_cnt
        
    def app_isinit_rate(self):
        total_cnt  = self.m_origin_data.shape[0]
        isinit_cnt = 0
        for i in range(total_cnt):
            install_type = self.m_origin_data.iloc[i]["type"]
            if int(install_type) == 0:
                isinit_cnt += 1
        return isinit_cnt*1.0/total_cnt

    def app_isinstall_rate(self):
        total_cnt  = self.m_origin_data.shape[0]
        isinstall_cnt = 0
        for i in range(total_cnt):
            install_type = self.m_origin_data.iloc[i]["type"]
            if int(install_type) == 1:
                isinstall_cnt += 1
        return isinstall_cnt*1.0/total_cnt

    def app_interval_hours(self):
        app_nanopay_time = None
        for i in range(self.m_origin_data.shape[0]):
            appname      = self.m_origin_data.iloc[i]["appname"].lower()
            install_time = self.m_origin_data.iloc[i]["timestamps"]
            if appname == "nanopay":
                app_nanopay_time = install_time
                break

        msg,flag,app_dt = time2datt(app_nanopay_time,_unit="ms")
        msg,flag,end_dt = time2datt(self.m_end_time,_unit="ms")
        total_seconds   = (end_dt-app_dt).total_seconds()
        dst             = int(total_seconds/3600)
        return dst

    def app_isbank_rate(self):
        """
        if True:
            print("enter app_isbank_rate::")
            print("model_app_type_dict::",len(model_app_type_dict))
            debug_line()
        """

        total_cnt   = self.m_origin_data.shape[0]
        isbank_cnt  = 0
        for i in range(total_cnt):
            appname      = self.m_origin_data.iloc[i]["appname"]
            apptype      = model_app_type_dict.get(appname,"")
            ##if True:
            ##    print("\t","i==",i,appname,apptype)
            if apptype == "bank":
                isbank_cnt += 1
        return isbank_cnt*1.0/total_cnt

    def app_isloan_rate(self):
        total_cnt   = self.m_origin_data.shape[0]
        isloan_cnt  = 0
        for i in range(total_cnt):
            appname      = self.m_origin_data.iloc[i]["appname"]
            apptype      = model_app_type_dict.get(appname,"")
            if apptype == "loan":
                isloan_cnt += 1
        return isloan_cnt*1.0/total_cnt

    def app_isjingpin_rate(self):
        total_cnt       = self.m_origin_data.shape[0]
        isjingpin_cnt   = 0
        for i in range(total_cnt):
            appname      = self.m_origin_data.iloc[i]["appname"]
            apptype      = model_app_type_dict.get(appname,"")
            if apptype == "jingpin":
                isjingpin_cnt += 1
        return isjingpin_cnt*1.0/total_cnt

    def app_isloan_night_rate(self):
        total_cnt    = self.m_origin_data.shape[0]
        isloan_cnt   = 0
        night_cnt    = 0
        for i in range(total_cnt):
            appname         = self.m_origin_data.iloc[i]["appname"]
            install_timestr = self.m_origin_data.iloc[i]["installtime_utc"]
            apptype         = model_app_type_dict.get(appname,"")
            if apptype == "loan":
                isloan_cnt += 1
                install_dt = time.strptime(install_timestr, "%Y-%m-%d %H:%M:%S")
                if install_dt.tm_hour >= 19 or install_dt.tm_hour<=6:
                    night_cnt += 1
        if isloan_cnt == 0:
            return 0.0
        else:
            return night_cnt*1.0/isloan_cnt


    def app_isloan_day_rate(self):
        total_cnt    = self.m_origin_data.shape[0]
        isloan_cnt   = 0
        day_cnt      = 0
        for i in range(total_cnt):
            appname         = self.m_origin_data.iloc[i]["appname"]
            install_timestr = self.m_origin_data.iloc[i]["installtime_utc"]
            apptype         = model_app_type_dict.get(appname,"")
            if apptype == "loan":
                isloan_cnt += 1
                install_dt = time.strptime(install_timestr, "%Y-%m-%d %H:%M:%S")
                if install_dt.tm_hour < 19 and install_dt.tm_hour>6:
                    day_cnt += 1
        if isloan_cnt == 0:
            return 0.0
        else:
            return day_cnt*1.0/isloan_cnt

