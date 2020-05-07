# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from AVGame import AVGame


class Avatar(KBEngine.Entity, AVGame, ):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        AVGame.__init__(self)

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------
    def onDestroy(self):
        # 清理引用
        self.cellRoom = None
    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    
    # ---------------------------------------------------
    # 		cell 接口
    # ---------------------------------------------------
    

    # ---------------------------------------------------
    # 		CExs 接口
    # ---------------------------------------------------