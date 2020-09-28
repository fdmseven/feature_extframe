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
import datetime
from utils.local_config import logger
from utils.local_config import feaconf

from fdm_utils.common             import get_tb_info
from fdm_utils.common             import debug_line
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## 函数部分
## time2datt                    时间戳转为datetime
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def time2datt(_time_stamp,_unit="s",_flag_utc=False):
    msg  = "success"
    flag = 0
    dst  = None
    try:
        time_stamp = 0
        if _unit=="s":
            time_stamp = int(_time_stamp)
        elif _unit=="ms":
            time_stamp = int(_time_stamp)/1000
        else:
            time_stamp = int(_time_stamp)

        if _flag_utc:
            dst = datetime.datetime.utcfromtimestamp(time_stamp)
        else:
            dst = datetime.datetime.fromtimestamp(time_stamp)
    except:
        msg  = get_tb_info()
        flag = -1
        dst  = None
    return msg,flag,dst
