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

from fdmutils.common import get_tb_info
from fdmutils.common import debug_line

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## 变量部分
## tag_app_type_dict        ##记录app类型的字典，从tag目录中解析
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
CURRENT_DIR     = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR        = os.path.join(CURRENT_DIR, '../../')
TAG_DIR         = os.path.join(ROOT_DIR, './tag')
sys.path.insert(0,TAG_DIR)
from  app_type import tag_app_type_dict
