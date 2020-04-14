# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from halls import halls

class chessHalls(halls):
    def __init__(self):
        halls.__init__(self)

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------

    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def _createRoom(self, roomType, avList):
        """
        创建房间
        参数1：房间类型
        参数2：房间内玩家列表
        """
        ERROR_MSG("chessHalls::_createRoom(%s)." % (avList))
    
    # ---------------------------------------------------
    # 		Base 接口
    # ---------------------------------------------------
    
    
    