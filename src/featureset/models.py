# encoding: utf-8

import datetime
import os
import sys
import time
from utils.local_config import logger
from utils.local_config import feaconf

from fdm_utils.common             import get_tb_info

class CFeature(object):

    def __init__(self,_origin_data=None,_key=None,_value=None,_end_time=None):
        self.m_key          = _key
        self.m_value        = _value
        self.m_isinit_bool  = False
        self.m_flag         = "model"
        self.m_fid_list     = []
        self.m_end_time     = _end_time
        self.m_feature_map  = {
            1: self.hello,
        }
    
    def hello(self):
        print("CFeature:hello")
        return 0

    def init(self):
        pass

    def extract(self):
        self.init()
        
        begin_time  = time.time()
        resmap      = {}
        for idl in self.m_fid_list:
            idl  = int(idl)
            if idl in self.m_feature_map:
                time1 = time.time()
                try:
                    value = self.m_feature_map[idl]()
                
                    resmap[int(idl)] = str(value)
                except:
                    logger.error("%s=%s,fid=%d\n错误信息为[%s]" % (self.m_key,self.m_value,idl,get_tb_info()))
                    resmap[int(idl)] = "-9999"
                time2 = time.time()
                logger.debug("%s=%s,fid=%d,cost=%f秒" % (self.m_key,self.m_value,idl,time2-time1))
        end_time = time.time()
        logger.info("%s=%s,%s特征,cost=%f秒" % (self.m_key,self.m_value,self.m_flag,end_time-begin_time))
        return resmap

if __name__ == "__main__":
    pass
