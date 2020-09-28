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


from fdm_utils.common import get_tb_info
from fdm_utils.common import debug_line
from fdm_utils.config import init_log_from_config
from fdm_utils.config import read_config

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## 变量部分
## logger               ##打印日志的全局变量，从log.conf中解析 
## feaconf              ##特征配置的全局变量，从feature.conf中解析 
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
CURRENT_DIR      = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR         = os.path.join(CURRENT_DIR, '../../')
CONFIG_LOG       = os.path.join(ROOT_DIR,"conf/log.conf")
CONFIG_FEATURE   = os.path.join(ROOT_DIR,"conf/feature.conf")

msg,flag,logger  = init_log_from_config(CONFIG_LOG,_root_dir=ROOT_DIR)
msg,flag,feaconf = read_config(CONFIG_FEATURE)

