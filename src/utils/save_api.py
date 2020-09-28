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
## save_feature             保存特征结果
## save_data                保存原始数据
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def save_feature(_key="user_id",_value=None,_feature_dict={},_fout=None,_head=True):
    msg  = "success"
    flag = 0

    try:
        key_list    = []
        value_list  = []
        for key in sorted(_feature_dict.keys()):
            key_list.append(str(key))
            value_list.append(str(_feature_dict[key]))

        key_list.append(str(_key))          ##添加user_id
        value_list.append(str(_value))      ##添加user_id的值

        if _head:
            _fout.write("%s\n" % (",".join(key_list)))
        _fout.write("%s\n" % (",".join(value_list)))
    except:
        logger.error("%s=%s,save_feature失败" % (_key,_value))
        msg  = get_tb_info()
        flag = -1
    return msg,flag

def save_data(_key="user_id",_value=None,_data_df=None,_fout=None,_head=True,_sp_row=","):
    flag = 0
    msg  = "success"
    try:
        _data_df[_key]  = _value
        
        columns         = list(_data_df.columns)
        fieldkey_dict   = {}
        for i in range(len(columns)):
            item = columns[i]
            fieldkey_dict[item] = i

        if _head:
            _fout.write("%s\n" % (_sp_row.join(columns)))
        for i in range(_data_df.shape[0]):
            data_list = []
            for item in columns:
                value = str(_data_df.iloc[i][item])
                data_list.append(value.replace(",","|").replace("\r\n"," ").replace("\n"," "))
            _fout.write("%s\n" % (_sp_row.join(data_list)))
            ##_fout.write("get_one\n")
        ##_fout.write("get_item\n")
    except:
        logger.error("%s=%s,save_data失败" % (_key,_value))
        msg  = get_tb_info()
        flag = -1
        print("msg==")
        print(msg)
        debug_line()
    return msg,flag
