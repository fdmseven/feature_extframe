#coding=utf-8
import os
import sys
import time
from utils.data_api      import get_basic_data              ## 获取基础数据[basic]
from utils.data_api      import get_sms_data                ## 获取短信数据[sms]
from utils.data_api      import get_app_data                ## 获取app数据[app]
from utils.save_api      import save_feature                ## 保存特征，以保存到文件为例。
from utils.save_api      import save_data                   ## 保存数据，以保存到文件为例。
from featureset.basic    import CBasicFeature               ## 基础数据的特征类
from featureset.app      import CAppFeature                 ## app数据的特征类
from featureset.sms      import CSmsFeature                 ## 短信数据的特征类
from utils.local_config  import logger                      ## 打印日志的全局变量，从log.conf中解析
from utils.local_config  import feaconf                     ## 特征配置的全局变量，从feature.conf中解析

from fdm_utils.common                 import get_tb_info                 ## 异常处理
from fdm_utils.common                 import show_dict_intree            ## 特征可视化 => 【以树的形式，可视化一个字典】
from fdm_utils.common                 import debug_line                  ## 打印空行，屏幕输出间隔开，方便调试


class CFeatureExtractObj():
    def __init__(self):
        self.m_origin_data_dict = {}        ##原始数据，需要获取
        self.m_feature_dict     = {}        ##特征相关，需要获取

        self.m_useful_dict      = {}        ##用于筛选
        self.m_sp_row           = ","       ##分隔符
        pass

    def init(self):
        self.m_useful_dict["basic"]     = 1
        self.m_useful_dict["app"]       = 1
        self.m_useful_dict["sms"]       = 1
        pass

    def getOriginData(self,_key="user_id",_value=None,_end_time=None):
        self.m_origin_data_dict = {}
        for datatype in self.m_useful_dict.keys():
            if datatype=="basic":
                msg,flag,self.m_origin_data_dict[datatype] = get_basic_data(_key=_key,_value=_value,_end_time=_end_time)
            if datatype=="app":
                msg,flag,self.m_origin_data_dict[datatype] = get_app_data(_key=_key,_value=_value,_end_time=_end_time)
            if datatype=="sms":
                msg,flag,self.m_origin_data_dict[datatype] = get_sms_data(_key=_key,_value=_value,_end_time=_end_time)



    def getFeature(self,_key="user_id",_value=None,_end_time=None):
        self.m_feature_dict = {}
        for datatype in self.m_useful_dict.keys():
            if datatype=="basic":
                basic_data = self.m_origin_data_dict.get(datatype,{})
                basic_obj  = CBasicFeature(_origin_data=basic_data,_key=_key,_value=_value,_end_time=_end_time)
                basic_obj.init()
                self.m_feature_dict.update(basic_obj.extract())
            if datatype=="app":
                app_data = self.m_origin_data_dict.get(datatype,{})
                app_obj = CAppFeature(_origin_data=app_data,_key=_key,_value=_value,_end_time=_end_time)
                app_obj.init()
                self.m_feature_dict.update(app_obj.extract())
            if datatype=="sms":
                sms_data = self.m_origin_data_dict.get(datatype,{})
                sms_obj  = CSmsFeature(_origin_data=sms_data,_key=_key,_value=_value,_end_time=_end_time)
                sms_obj.init()
                self.m_feature_dict.update(sms_obj.extract())


    def showOriginData(self,_datatype):
        origin_data = self.m_origin_data_dict.get(_datatype,{})
        print("%s数据::" % (_datatype),type(origin_data))
        print(origin_data)
        debug_line() 

    def showFeature(self):
        show_dict_intree(self.m_feature_dict)
        debug_line() 

    def saveFeature(self,_key=None,_value=None,_fout=None,_head=False):
        msg,flag = save_feature(_key=_key,_value=_value,_feature_dict=self.m_feature_dict,_fout=_fout,_head=_head)
        debug_line() 

    def saveOriginData(self,_key=None,_value=None,_fout=None,_head=False,_datatype=""):
        if self.m_useful_dict.get(_datatype,0):
            data_df = self.m_origin_data_dict.get(_datatype,{})
            if True:
                print("enter saveOriginData::")
                print("data_df::",type(data_df))
                debug_line()
            save_data(_key=_key,_value=_value,_data_df=data_df,_fout=_fout,_head=_head,_sp_row=self.m_sp_row)

        debug_line() 


if __name__ == "__main__":
    print("call CFeatureExtractObj")
    sys.exit(0)
