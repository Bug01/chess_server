# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from AVGobang import AVGobang

class AVGame(AVGobang):
    def __init__(self):
        AVGobang.__init__(self)
        
        # 角色的座位号
        self.pub_chairID = 0

        # 角色准备状态
        self.pub_ready = False

        # 角色在线状态
        self.pub_online = True

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------

    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def setChairID(self, chairID):
        """
        设置角色座位号
        参数1：角色座位号
        """
        self.pub_chairID = chairID

    def getChairID(self):
        """
        获取角色座位号
        """
        return self.pub_chairID

    def setReady(self):
        """
        设置准备状态
        """
        self.pub_ready = True

    def getReady(self):
        """
        获取准备状态
        """
        return self.pub_ready

    def getOnline(self):
        """
        获取在线状态
        """
        return self.pub_online
    
    # ---------------------------------------------------
    # 		cell 接口
    # ---------------------------------------------------
    def C_tellOnlineStatus(self, bOnline):
        """
        通知在线/下线状态
        参数1：是否在线
        """
        self.pub_online = bOnline

    # ---------------------------------------------------
    # 		CExs 接口
    # ---------------------------------------------------
    def CExs_reqLoadDone(self):
        """
        通知加载完成
        """
        # 通知加入房间
        self.cellRoom.reqLoadDone(self.cellAvatrID, self)

    def CExs_reqReady(self):
        """
        通知准备游戏
        """
        # 设置准备
        self.setReady()

        # 通知准备游戏
        self.cellRoom.reqReady(self.cellAvatrID, self)






