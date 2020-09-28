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
from utils.time_api     import time2datt

from fdm_utils.common             import get_tb_info
from fdm_utils.common             import debug_line
from fdm_utils.common             import is_number

class CSmsFeature(CFeature):
    def __init__(self,_origin_data=None,_key=None,_value=None,_end_time=None):
        self.m_key          = _key
        self.m_value        = _value
        self.m_origin_data  = _origin_data
        self.m_feaconf       = feaconf
        self.m_end_time     = _end_time
        self.m_feature_map  = {
            ###########################
            50001000:self.sms_count,                ##50001000 = 短信数量
            50002000:self.sms_send_rate,            ##50002000 = 短信中发送的占比
            50003000:self.sms_receive_rate,         ##50003000 = 短信中接收的占比
            50004000:self.sms_read_rate,            ##50004000 = 短信的已读占比
            50005000:self.sms_timeone_rate,         ##50005000 = 短信的时间占比【00-06】
            50006000:self.sms_timetwo_rate,         ##50006000 = 短信的时间占比【06-12】
            50007000:self.sms_timethree_rate,       ##50007000 = 短信的时间占比【12-18】
            50008000:self.sms_timefour_rate,        ##50008000 = 短信的时间占比【18-24】
            50009000:self.sms_link_rate,            ##50009000 = 短信中对话方式的占比（发送收件人是同一人）
            50010000:self.sms_numberone_rate,       ##50010000 = 短信号码的比例分布【短号码】
            50011000:self.sms_numbertwo_rate,       ##50011000 = 短信号码的比例分布【长号码】
            50012000:self.sms_numberthree_rate,     ##50012000 = 短信号码的比例分布【名称类】
            50013000:self.sms_interval_hours_max,   ##50013000 = 包含nanopay与授信时间的间隔小时数最大值
            50014000:self.sms_interval_hours_min,   ##50014000 = 包含nanopay与授信时间的间隔小时数最小值
        }
        pass

    def init(self):
        self.m_fid_list = self.m_feaconf['sms']
        self.m_flag     = "sms"
        pass

    ###################################
    ## 特征计算的函数
    ###################################
    def sms_count(self):
        dst = self.m_origin_data.shape[0]
        return dst

    def sms_send_rate(self):
        total_cnt = self.m_origin_data.shape[0]
        send_cnt  = 0
        for i in range(total_cnt):
            sms_send_type = self.m_origin_data.iloc[i]["type"]
            if int(sms_send_type) == 1:
                send_cnt += 1
        return send_cnt*1.0/total_cnt

    def sms_receive_rate(self):
        total_cnt = self.m_origin_data.shape[0]
        recv_cnt  = 0
        for i in range(total_cnt):
            sms_send_type = self.m_origin_data.iloc[i]["type"]
            if int(sms_send_type) == 2:
                recv_cnt += 1
        return recv_cnt*1.0/total_cnt

    def sms_read_rate(self):
        total_cnt = self.m_origin_data.shape[0]
        read_cnt  = 0
        for i in range(total_cnt):
            read_type = self.m_origin_data.iloc[i]["read"]
            if int(read_type) == 1:
                read_cnt += 1
        return read_cnt*1.0/total_cnt

    def sms_timeone_rate(self):
        total_cnt    = self.m_origin_data.shape[0]
        timeone_cnt  = 0
        for i in range(total_cnt):
            sms_time        = self.m_origin_data.iloc[i]["time"]
            msg,flag,sms_dt = time2datt(sms_time,_unit="s")
            sms_hour        = sms_dt.hour
            if sms_hour >= 0 and sms_hour <= 6:
                timeone_cnt += 1
        return timeone_cnt*1.0/total_cnt

    def sms_timetwo_rate(self):
        total_cnt    = self.m_origin_data.shape[0]
        timetwo_cnt  = 0
        for i in range(total_cnt):
            sms_time        = self.m_origin_data.iloc[i]["time"]
            msg,flag,sms_dt = time2datt(sms_time,_unit="s")
            sms_hour        = sms_dt.hour
            if sms_hour >= 7 and sms_hour <= 12:
                timetwo_cnt += 1
        return timetwo_cnt*1.0/total_cnt

    def sms_timethree_rate(self):
        total_cnt    = self.m_origin_data.shape[0]
        timethree_cnt  = 0
        for i in range(total_cnt):
            sms_time        = self.m_origin_data.iloc[i]["time"]
            msg,flag,sms_dt = time2datt(sms_time,_unit="s")
            sms_hour        = sms_dt.hour
            if sms_hour >= 13 and sms_hour <= 18:
                timethree_cnt += 1
        return timethree_cnt*1.0/total_cnt

    def sms_timefour_rate(self):
        total_cnt    = self.m_origin_data.shape[0]
        timefour_cnt  = 0
        for i in range(total_cnt):
            sms_time        = self.m_origin_data.iloc[i]["time"]
            msg,flag,sms_dt = time2datt(sms_time,_unit="s")
            sms_hour        = sms_dt.hour
            if sms_hour >= 19 and sms_hour <= 24:
                timefour_cnt += 1
        return timefour_cnt*1.0/total_cnt
    
    def sms_link_rate(self):
        total_cnt = self.m_origin_data.shape[0]
        link_cnt  = 0

        send_list = []
        recv_list = []
        for i in range(total_cnt):
            sms_send_type = self.m_origin_data.iloc[i]["type"]
            addr          = self.m_origin_data.iloc[i]["addr"]
            if int(sms_send_type) == 1:
                send_list.append(addr)
            if int(sms_send_type) == 2:
                recv_list.append(addr)

        for item in send_list:
            if item in recv_list:
                link_cnt += 1
        return link_cnt*1.0/total_cnt

    def sms_numberone_rate(self):
        total_cnt       = self.m_origin_data.shape[0]
        numberone_cnt   = 0
        for i in range(total_cnt):
            addr = self.m_origin_data.iloc[i]["addr"]
            addr = addr.replace("+91","")
            if is_number(addr) and len(addr)<=5:
                numberone_cnt += 1
        return numberone_cnt*1.0/total_cnt

    def sms_numbertwo_rate(self):
        total_cnt       = self.m_origin_data.shape[0]
        numbertwo_cnt   = 0
        for i in range(total_cnt):
            addr = self.m_origin_data.iloc[i]["addr"]
            addr = addr.replace("+91","")
            if is_number(addr) and len(addr)>=9:
                numbertwo_cnt += 1
        return numbertwo_cnt*1.0/total_cnt

    def sms_numberthree_rate(self):
        total_cnt       = self.m_origin_data.shape[0]
        numberthree_cnt   = 0
        for i in range(total_cnt):
            addr = self.m_origin_data.iloc[i]["addr"]
            addr = addr.replace("+91","")
            if not is_number(addr):
                numberthree_cnt += 1
        return numberthree_cnt*1.0/total_cnt

    def sms_interval_hours_max(self):
        sms_nanopay_max_time = None
        max_time             = 0
        for i in range(self.m_origin_data.shape[0]):
            body     = self.m_origin_data.iloc[i]["body"]
            sms_time = self.m_origin_data.iloc[i]["time"]
            if "<Nanopay>" in body or "[Nanopay]" in body:
                if sms_time > max_time:
                    max_time             = sms_time
                    sms_nanopay_max_time = max_time

        msg,flag,max_sms_dt = time2datt(sms_nanopay_max_time,_unit="s")
        msg,flag,end_dt     = time2datt(self.m_end_time,_unit="ms")
        total_seconds   = (end_dt - max_sms_dt).total_seconds()
        dst             = int(total_seconds/3600)
        return dst


    def sms_interval_hours_min(self):
        sms_nanopay_min_time = None
        min_time             = self.m_end_time

        for i in range(self.m_origin_data.shape[0]):
            body     = self.m_origin_data.iloc[i]["body"]
            sms_time = self.m_origin_data.iloc[i]["time"]
            if "<Nanopay>" in body or "[Nanopay]" in body:
                if sms_time < min_time:
                    min_time             = sms_time
                    sms_nanopay_min_time = min_time

        msg,flag,min_sms_dt = time2datt(sms_nanopay_min_time,_unit="s")
        msg,flag,end_dt     = time2datt(self.m_end_time,_unit="ms")
        total_seconds   = (end_dt - min_sms_dt).total_seconds()
        dst             = int(total_seconds/3600)
        return dst

