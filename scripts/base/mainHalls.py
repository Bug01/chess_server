# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GTools

class mainHalls(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)

        # 已经注册的大厅信息
        self.hallsDict = {}

        # 在线的角色字典
        self.avatarsDict = {}

        # 注册自己到base层的全局
        GTools.setBaseData_MainHalls(self)

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
        DEBUG_MSG("%s(%i):onTimer. tid(%s) userArg(%s)." % (self.entityName, self.id, tid, userArg))

    # ---------------------------------------------------
    # 		Base method
    # ---------------------------------------------------
    def B_tellHallsInfo(self, hallsEnMB, hallsName):
        """
        通知大厅信息
        参数1：大厅的EntityCall
        参数2：大厅的名字
        """
        INFO_MSG("%s(%i):B_tellHallsInfo. hallsName(%s)." % (self.entityName, self.id, hallsName))

        self.hallsDict[hallsName] = hallsEnMB

    def B_tellOnline(self, reqEnMB, reqDBID):
        """
        通知上线
        参数1：角色EntityCall
        参数2：角色DBID
        """
        INFO_MSG("%s(%i):B_tellOnline. reqDBID(%i)." % (self.entityName, self.id, reqDBID))

        # 增加角色信息
        self.avatarsDict[reqDBID] = reqEnMB
        

    def B_tellOffline(self, reqEnMB, reqDBID):
        """
        通知离线
        参数1：角色EntityCall
        参数2：角色DBID
        """
        INFO_MSG("%s(%i):B_tellOffline. reqDBID(%i)." % (self.entityName, self.id, reqDBID))

        # 角色不存在
        if self.avatarsDict.get(reqDBID) is None:
            ERROR_MSG("%s(%i):B_tellOffline. reqDBID(%i) not in halls." % (self.entityName, self.id, reqDBID))
            return

        # 删除角色信息
        del self.avatarsDict[reqDBID]

    def B_reqEnterGameHalls(self, reqEnMB, reqDBID, hallsName):
        """
        请求加入游戏大厅
        参数1：角色EntityCall
        参数2：角色DBID
        参数3：要加入的游戏大厅名称
        """
        # 游戏大厅不存在
        halls = self.hallsDict.get(hallsName)
        if halls is None:
            ERROR_MSG("%s(%i):B_reqEnterHalls. hallsName(%s) err." % (self.entityName, self.id, hallsName))
            return

        # 请求加入大厅
        halls.B_reqEnterHalls(reqEnMB, reqDBID)

        
    