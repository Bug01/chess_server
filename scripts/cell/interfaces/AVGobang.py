# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class AVGobang:
    def __init__(self):
        
        # 最后一步落子位置
        self.lastPos_x = 0
        self.lastPos_y = 0

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
        self.lastPos_x = 0
        self.lastPos_y = 0
    
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

    def CExs_reqDraw(self, bCanEnd):
        """
        请求和棋
        参数1：是否同意和棋
        """
        self.cellRoom.reqDraw(self.cellAvatrID, self, bCanEnd)

    def CExs_reqBackChess(self, backType):
        """
        请求悔棋
        参数1：悔棋类型 
                1：请求悔棋
                2：同意悔棋
                3：不同意悔棋
        """
        self.cellRoom.reqBackChess(self.cellAvatrID, self, backType)



