# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GDefine

class AVGobang:
    def __init__(self):
        
        # 最后一步落子位置
        self.lastPos_x = GDefine.GC_ERROR_POS
        self.lastPos_y = GDefine.GC_ERROR_POS

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------

    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def lastChessPos(self, x, y):
        """
        最后落子位置
        参数1：x位置
        参数2：y位置
        """
        self.lastPos_x = x
        self.lastPos_y = y
    
    def clearLastChess(self):
        self.lastPos_x = GDefine.GC_ERROR_POS
        self.lastPos_y = GDefine.GC_ERROR_POS
    
    # ---------------------------------------------------
    # 		cell 接口
    # ---------------------------------------------------

    # ---------------------------------------------------
    # 		CExs 接口
    # ---------------------------------------------------
    def CExs_reqChess(self, pos_x, pos_y):
        """
        通知下子
        参数1：下子位置x
        参数2：下子位置y
        """
        # 通知准备游戏
        self.cellRoom.reqChess(self.cellAvatrID, self, pos_x, pos_y)


    def CExs_reqConsent(self, tp):
        """
        请求对方同意
        参数1：请求类型
                1：和棋
                2：悔棋
        """
        # 请求和棋
        if tp == 1:
            self.cellRoom.reqDraw(self.cellAvatrID, self, tp)
        # 请求悔棋
        elif tp == 2:
            self.cellRoom.reqBackChess(self.cellAvatrID, self, tp)

    def CExs_reqConsentBack(self, tp, bAgree):
        """
        请求回应对方是否同意
        参数1：回应类型
                1：和棋
                2：悔棋
        参数2：是否同意
        """
        # 请求和棋
        if tp == 1:
            self.cellRoom.reqDrawBack(self.cellAvatrID, self, tp, bAgree)
        # 请求悔棋
        elif tp == 2:
            self.cellRoom.reqBackChessBack(self.cellAvatrID, self, tp, bAgree)

    def CExs_reqLose(self):
        """
        请求认输
        """
        self.cellRoom.reqLose(self.cellAvatrID, self)
