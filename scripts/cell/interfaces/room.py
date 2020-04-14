# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GDefine


class room(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)

        # 房间内玩家 { DBID : EntityCall }
        self.cellAvatars = {}

        # 房间内玩家 { chairID : EntityCall }
        self.chairAvatars = {}

        # 当前操作的位置
        self.curChairID = 0

        # 当前游戏状态
        self.curRoomStatus = GDefine.GC_RoomStatus['free']

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------
    def onDestroy(self):
        # 清理引用
        self.cellAvatars.clear()
        self.chairAvatars.clear()
    
    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def _getEmptyChairID(self):
        """
        获取一个空座位号
        """
        for chairID in range(1, self.cellMaxPlayerCount + 1):
            if chairID not in self.chairAvatars:
                return chairID

        return 0

    def _inGame(self):
        """
        是否在游戏中
        """
        return self.curRoomStatus == GDefine.GC_RoomStatus['game']

    def reqLoadDone(self, reqDBID, reqCellEnMB):
        """
        通知角色加载完成
        参数1：角色的DBID
        参数2：角色的cellCall
        """
        # 当前房间人数是否满了
        if len(self.cellAvatars) >= self.cellMaxPlayerCount:
            ERROR_MSG("%s(%i)reqLoadDone: reqDBID(%i) but players full." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 记录房间内玩家
        self.cellAvatars[reqDBID] = reqCellEnMB

        # 获取一个可用座位号
        chairID = self._getEmptyChairID()
        self.chairAvatars[chairID] = reqCellEnMB

        # 通知座位号
        reqCellEnMB.setChairID(chairID)

    def reqReady(self, reqDBID, reqCellEnMB):
        """
        通知角色准备游戏
        参数1：角色的DBID
        参数2：角色的cellCall
        """
        # 检查房间人数
        if len(self.chairAvatars) != self.cellMaxPlayerCount:
            return

        # 检查准备人数
        for av in self.chairAvatars.values():
            if not av.getReady():
                return

        # 开始游戏
        self.onStartGame()

    def onStartGame(self):
        """
        开始游戏
        """
        self.curRoomStatus = GDefine.GC_RoomStatus['game']

    def onEndGame(self, winPos):
        """
        结束游戏
        参数1：赢家位置
        """
        self.curRoomStatus = GDefine.GC_RoomStatus['end']

    def destroyRoom(self):
        """
        销毁房间实体
        """
        for av in self.cellAvatars.values():
            av.destroy()

        self.destroy()
        
    # ---------------------------------------------------
    # 		cell method
    # ---------------------------------------------------
    
    
    