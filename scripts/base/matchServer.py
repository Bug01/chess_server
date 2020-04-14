# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GDefine

class matchServer(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)

        # 匹配池
        self.matchPoll = {}

        # 通知大厅匹配实体创建成功
        self.masterHalls.B_tellMatchServer(self, self.roomType)

        # 定时检查匹配
        self.addTimer(GDefine.GC_MatchTime['matchInterval']['initialOffset'],
                        GDefine.GC_MatchTime['matchInterval']['repeatOffset'],
                        GDefine.GC_MatchTime['matchInterval']['userArg'])


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
        # 向主大厅上报自己信息 上报完成后停止
        if userArg == GDefine.GC_MatchTime['matchInterval']['userArg']:
            self._startMatch()

    # ---------------------------------------------------
    # 		内部 接口
    # ---------------------------------------------------
    def _startMatch(self):
        num = 2
        while len(self.matchPoll) >= num:
            avList = []
            # 提取匹配结果
            for reqDBID in self.matchPoll:
                avList.append(self.matchPoll[reqDBID])
                if len(avList) == num:
                    break
            
            # 从匹配池删除匹配的结果
            for k in avList:
                self.matchPoll.pop(k['reqDBID'], None)

            # 通知大厅匹配结果
            self.masterHalls.B_tellMatchResult(self.roomType, avList)

    # ---------------------------------------------------
    # 		Base 接口
    # ---------------------------------------------------
    def B_reqStartMatch(self, reqEnMB, reqDBID, matchInfo):
        """
        请求匹配
        参数1：角色EntityCall
        参数2：角色DBID
        参数3：角色的匹配信息
        """
        # 添加到匹配池
        self.matchPoll[reqDBID] = {
                                    'reqEnMB' : reqEnMB, 
                                    'reqDBID' : reqDBID, 
                                    'matchInfo' : matchInfo
                                }

        # 通知结果
        reqEnMB.B_ackMatchRoom(True, "请求成功", self.roomType)

    def B_reqCancelMatch(self, reqEnMB, reqDBID):
        """
        请求匹配
        参数1：角色EntityCall
        参数2：角色DBID
        """
        # 删除匹配池信息
        self.matchPoll.pop(reqDBID, None)

        # 通知结果
        reqEnMB.B_ackCancelMatch(True, "请求成功")
    
    
        
    