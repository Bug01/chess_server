# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GTools
import GDefine

class halls(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)

        # 大厅的角色
        self.avatars = {}

        # 大厅匹配服务
        self.matchServers = {}

        # 初始化匹配实体
        self._initMatchServer()

        # 向主大厅上报自己的信息
        self.addTimer(GDefine.GC_HallsTime['regToMainHalls']['initialOffset'],
                        GDefine.GC_HallsTime['regToMainHalls']['repeatOffset'],
                        GDefine.GC_HallsTime['regToMainHalls']['userArg'])

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
        DEBUG_MSG("%s(%i):onTimer. tid(%s) userArg(%s)." % (self.hallsName, self.id, tid, userArg))

        # 向主大厅上报自己信息 上报完成后停止
        if userArg == GDefine.GC_HallsTime['regToMainHalls']['userArg']:
            mainHalls = GTools.getBaseData_MainHalls()
            if mainHalls:
                mainHalls.B_tellHallsInfo(self, self.hallsName)
                self.delTimer(tid)
    
    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def _initMatchServer(self):
        """
        初始化匹配实体
        """
        for roomType in GDefine.GC_RoomType.values():
            # 自建房不需要匹配服务
            if roomType == GDefine.GC_RoomType['Create']:
                continue

            param = {
                'roomType'		: roomType,
                'masterHalls'	: self,
            }

            KBEngine.createEntityAnywhere('matchServer', param)
    # ---------------------------------------------------
    # 		Base method
    # ---------------------------------------------------
    def B_tellMatchServer(self, matchServer, roomType):
        """
        通知匹配服务实体
        参数1：匹配服务EntityCall
        参数2：匹配服务类型
        """
        # 记录匹配服务
        self.matchServers[roomType] = matchServer

    def B_reqEnterHalls(self, reqEnMB, reqDBID):
        """
        请求加入大厅
        参数1：角色EntityCall
        参数2：角色DBID
        """
        self.avatars[reqDBID] = reqEnMB
        
        # 通知加入大厅
        reqEnMB.B_ackEnterHalls(self, self.hallsName)

    def B_reqMatchRoom(self, reqEnMB, reqDBID, roomType, matchInfo):
        """
        请求匹配房间
        参数1：角色EntityCall
        参数2：角色DBID
        参数3：房间类型
        参数4：角色的匹配信息
        """
        # 获取匹配服务
        matchSer = self.matchServers.get(roomType)

        # 没有相关的匹配服务
        if matchSer is None:
            reqEnMB.B_ackMatchRoom(False, "参数错误", 0)
            return

        # 开始匹配
        matchSer.B_reqStartMatch(reqEnMB, reqDBID, matchInfo)

    def B_reqCancelMatch(self, reqEnMB, reqDBID, roomType):
        """
        请求取消匹配
        参数1：角色EntityCall
        参数2：角色DBID
        参数3：房间类型
        """
        # 获取匹配服务
        matchSer = self.matchServers.get(roomType)

        # 没有相关的匹配服务
        if matchSer is None:
            reqEnMB.B_ackCancelMatch(False, "参数错误")
            return

        # 取消匹配
        matchSer.B_reqCancelMatch(reqEnMB, reqDBID)

    def B_tellMatchResult(self, roomType, avList):
        """
        通知匹配结果
        参数1：匹配类型
        参数2：匹配结果(玩家列表)
        """
        self._createRoom(roomType, avList)
    
    