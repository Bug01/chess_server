# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GDefine
import GTools


class room(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)

        # 房间内玩家 { DBID : EntityCall }
        self.cellAvatars = {}

        # 房间内玩家 { chairID : EntityCall }
        self.chairAvatars = {}

        # 当前操作的位置
        self.curChairID = 0

        # 房间定时器ID
        self.timerID = 0
        self.startTime = 0

        # 当前游戏状态
        self.curRoomStatus = GDefine.GC_RoomStatus['free']

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------
    def onTimer(self, tid, userArg):
        """
        KBEngine method.
        使用addTimer后， 当时间到达则该接口被调用
        @param tid		: addTimer 的返回值ID
        @param userArg	: addTimer 最后一个参数所给入的数据
        """
        self.onTimeout()

    def onDestroy(self):
        # 清理引用
        self.cellAvatars.clear()
        self.chairAvatars.clear()
    
    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def getEmptyChairID(self):
        """
        获取一个空座位号
        """
        for chairID in range(1, self.cellMaxPlayerCount + 1):
            if chairID not in self.chairAvatars:
                return chairID

        return 0

    def getAVByChairID(self, chairID):
        return self.chairAvatars.get(chairID)

    def inGame(self):
        """
        是否在游戏中
        """
        return self.curRoomStatus == GDefine.GC_RoomStatus['game']

    def resetTimer(self, initialOffset):
        """
        重置游戏定时器
        参数1：时间间隔
        """
        # 如果当前有定时器 先关闭
        if self.timerID != 0:
            self.closeTimer()

        # 开始定时器
        self.timerID = self.addTimer(initialOffset, 0, 0)
        self.startTime = GTools.nowTime()
        
    def closeTimer(self):
        """
        关闭定时器
        """
        if self.timerID != 0:
            self.delTimer(self.timerID)
            self.timerID = 0

    def onTimeout():
        """
        """
        pass

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
        chairID = self.getEmptyChairID()
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
        # 结束定时器
        self.closeTimer()

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
    
    
    