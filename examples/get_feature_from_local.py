#coding=utf-8
import os
import time
import sys

CURRENT_DIR     = os.path.abspath(os.path.dirname(__file__))
SRC_DIR         = os.path.join(CURRENT_DIR, '../src/')
sys.path.append(SRC_DIR)
from feature_extract        import CFeatureExtractObj
from utils.local_config     import logger                       ## 打印日志的全局变量，从log.conf中解析
from utils.local_config     import feaconf                      ## 特征配置的全局变量，从feature.conf中解析
from utils.data_api         import get_credit_time              ## 获取授信时间

from fdm_utils.common       import get_tb_info                  ## 异常处理
from fdm_utils.common       import debug_line                   ## 打印空行，屏幕输出间隔开，方便调试

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
## 参数设置（日志|特征）
## 选取一个用户测试
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
key             = "user_id"
value           = "id001"


begin_time      = time.time()
logger.info("%s=%s,begin" % (key,value))

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
## 特征提取类,初始化为对象
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
feature_obj     = CFeatureExtractObj()
feature_obj.init()

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
## 获取授信时间:
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
##msg,flag,credit_time = get_credit_time(_key=key,_value=value)
##print("credit_time==",credit_time,type(credit_time))
credit_time = None

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
## 获取原始数据:
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
feature_obj.getOriginData(_key=key,_value=value,_end_time=credit_time)
if True:
    print("查看原始数据::")
    feature_obj.showOriginData("basic")
    feature_obj.showOriginData("app")
    feature_obj.showOriginData("sms")
    

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
## 特征提取:
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
feature_obj.getFeature(_key=key,_value=value,_end_time=credit_time)
if True:
    print("查看特征提取结果::")
    feature_obj.showFeature()##特征打印出来看看


##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
## 程序完成，退出
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
end_time = time.time()
logger.info("%s=%s,finish,耗时=%f秒" % (key,value,end_time-begin_time))
print("\twork finish")
sys.exit(0)
