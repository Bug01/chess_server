# -*- coding: utf-8 -*-
# 工具函数
import KBEngine
from KBEDebug import *
import GServerCfg
import Functor
import copy
import time
import hashlib
import json


# 拷贝函数
def ecopy(v):
    return copy.copy(v)

# 深度拷贝函数
def dcopy(v):
    return copy.deepcopy(v)

# 时间
def nowTime():
    return int(time.time())

def functor(func, *args):
    return Functor.Functor(func, *args)

# 进行json格式化编码 dict转成str
def json_dumps(data):
    return json.dumps(data)

# 对json字符串进行解码 str转成dict
def json_load(data):
    return json.loads(data)

# byte转字符串
def byteToStr(data):
    return str(data, encoding = "utf-8")

# 注册主大厅
def setBaseData_MainHalls(entityCall):
    entityName = GServerCfg.GC_ServerEntity['mainHalls']['default']['entityName']
    KBEngine.baseAppData[entityName] = entityCall

# 获取主大厅
def getBaseData_MainHalls():
    entityName = GServerCfg.GC_ServerEntity['mainHalls']['default']['entityName']
    return KBEngine.baseAppData.get(entityName)

# 获取sha加密的数据
def getSha1Str(tarStr):
    return hashlib.sha1(tarStr.encode("utf8")).hexdigest()