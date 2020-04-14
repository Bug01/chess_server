# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GTools
import GDefine
import GServerCfg

class Avatar(KBEngine.Proxy):
    def __init__(self):
        KBEngine.Proxy.__init__(self)

        # 当前大厅
        self.nowHalls = None
        self.nowHallsName = ''

        # 当前房间
        self.nowRoomID = 0

        # 是否在匹配中及其房间类型
        self.bInMatch = False
        self.roomType = 0

        # 当前操作定时器
        self.opTimerID = 0

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------
    def onGetCell(self):
        """
        这个函数在它获得cell实体的时候被调用。
        """
        DEBUG_MSG("Avatar(%i_%i):onGetCell." % (self.id, self.avatarID))

    def onLoseCell(self):
        """
        这个函数在它关联的cell实体销毁之后被调用
        """
        DEBUG_MSG("Avatar(%i_%i):onLoseCell." % (self.id, self.avatarID))

        # 离开房间时
        self.nowRoomID = 0

    def onTimer(self, tid, userArg):
        """
        KBEngine method.
        使用addTimer后， 当时间到达则该接口被调用
        @param tid		: addTimer 的返回值ID
        @param userArg	: addTimer 最后一个参数所给入的数据
        """
        DEBUG_MSG("Avatar(%i_%i):onTimer. tid(%s) userArg(%s)." % (self.id, self.avatarID, tid, userArg))

        # 匹配请求超时 停止操作的定时器
        if userArg == GDefine.GC_AvatarTime['startMatchOp']['userArg']:
            self.opTimerID = 0
        
    def onClientEnabled(self):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        DEBUG_MSG("Avatar(%i_%i):onClientEnabled." % (self.id, self.avatarID))
        
        # 更新最后登陆时间
        self.lastReloginTime = GTools.nowTime()

        self._updateAvatar()

        # 获取主大厅失败
        mainHalls = GTools.getBaseData_MainHalls()
        if mainHalls is None:
            ERROR_MSG("Avatar(%i_%i):onClientEnabled. mainHalls is None." % (self.id, self.avatarID))
            return
        
        # 通知主大厅上线
        mainHalls.B_tellOnline(self, self.avatarID)
        
        # 当前游戏厅为空 则加入游戏大厅
        if self.nowHalls is None:
            hallsName = GServerCfg.GC_ServerIDToHalls[self.serverID]
            mainHalls.B_reqEnterGameHalls(self, self.avatarID, hallsName)
        
        # 当前游戏厅不为空 则通知当前所在大厅
        elif self.client is not None:
            self.client.Exs_tellCurHalls(self.nowHallsName)

        # 通知在线
        if self.cell is not None:
            self.cell.C_tellOnlineStatus(True)
        
    def onClientDeath(self):
        """
        KBEngine method.
        客户端对应实体已经销毁
        """
        DEBUG_MSG("Avatar(%i_%i):onClientDeath." % (self.id, self.avatarID))

        # 通知主大厅上线
        mainHalls = GTools.getBaseData_MainHalls()
        if mainHalls:
            mainHalls.B_tellOffline(self, self.avatarID)

        # 通知下线
        if self.cell is not None:
            self.cell.C_tellOnlineStatus(False)

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        DEBUG_MSG("Avatar(%i_%i):onDestroy." % (self.id, self.avatarID))

    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def _updateAvatar(self):
        """
        更新角色的基本信息
        """
        self.nickName = self.accountEntity.clientData['nickName']
        self.avatarUrl = self.accountEntity.clientData['avatarUrl']
        self.gender = self.accountEntity.clientData['gender']

    def _startOp(self, timerCfg):
        """
        开始操作
        """
        # 匹配超时
        if self.opTimerID == 0:
            self.opTimerID = self.addTimer(timerCfg['initialOffset'],
                                            timerCfg['repeatOffset'],
                                            timerCfg['userArg'])

    def _endOp(self):
        """
        结束操作
        """
        # 取消匹配超时
        if self.opTimerID != 0:
            self.delTimer(self.opTimerID)
            self.opTimerID = 0

    def _inOp(self):
        """
        是否在操作中
        """
        return self.opTimerID != 0

    def _setMatch(self, b):
        """
        设置匹配状态
        """
        self.bInMatch = b

    def _inMatch(self):
        """
        是否在匹配中
        """
        return self.bInMatch
    # ---------------------------------------------------
    # 		Base method
    # ---------------------------------------------------
    def B_ackEnterHalls(self, halls, hallsName):
        """
        通知加入大厅
        参数1：大厅的EntityCall
        参数2：大厅的名称
        """
        INFO_MSG("Avatar(%i_%i):B_ackEnterHalls hallsName(%s)." % (self.id, self.avatarID, hallsName))

        self.nowHalls = halls
        self.nowHallsName = hallsName

        # 通知当前所在大厅
        if self.client is not None:
            self.client.Exs_tellCurHalls(self.nowHallsName)

    def B_ackMatchRoom(self, bSucc, msg, roomType):
        """
        通知匹配请求结果
        参数1：请求是否成功
        参数2：相关消息
        参数3：匹配房间类型
        """
        INFO_MSG("Avatar(%i_%i):B_ackMatchRoom. bSucc(%s), msg(%s)" % (self.id, self.avatarID, bSucc, msg))

        # 结束操作
        self._endOp()

        # 匹配请求成功 开始匹配
        if bSucc:
            self._setMatch(True)
            self.roomType = roomType

        # 通知匹配结果
        if self.client is not None:
            self.client.Exs_ackStartMatch(bSucc, msg)

    def B_ackCancelMatch(self, bSucc, msg):
        """
        通知取消匹配结果
        参数1：是否成功
        参数2：相关消息
        """
        INFO_MSG("Avatar(%i_%i):B_ackCancelMatch. bSucc(%s), msg(%s)" % (self.id, self.avatarID, bSucc, msg))

        # 结束操作
        self._endOp()

        # 取消匹配成功 结束匹配
        if bSucc:
            self._setMatch(False)
            self.roomType = 0

        # 通知匹配结果
        if self.client is not None:
            self.client.Exs_ackCancelMatch(bSucc, msg)

    def B_tellJoinRoom(self, roomCell, roomID, gameID):
        """
        通知加入房间
        参数1：房间空间EntityCall(房间cell实体)
        参数2：房间号
        参数3：游戏ID
        """
        # 结束匹配状态
        self._setMatch(False)
        self.roomType = 0

        # 设置房间信息
        self.cellData['cellAvatrID'] = self.avatarID
        self.cellData['pub_nickName'] = self.nickName
        self.cellData['pub_avatarUrl'] = self.avatarUrl
        self.cellData['pub_gender'] = self.gender
        self.cellData['cellRoom'] = roomCell
        self.nowRoomID = roomID

        # 通知加入房间
        if self.client is not None:
            self.client.Exs_tellJoinRoom(gameID)
        
        # 创建cell层实体
        self.createCellEntity(roomCell)

    # ---------------------------------------------------
    # 		BExs method
    # ---------------------------------------------------
    def BExs_reqStartMatch(self, roomType):
        """
        请求开始匹配游戏
        参数1：房间类型
        """
        INFO_MSG("Avatar(%i_%i):BExs_reqStartMatch." % (self.id, self.avatarID))

        # 检查是否在房间中
        if self.nowRoomID != 0:
            ERROR_MSG("Avatar(%i_%i):BExs_reqStartMatch nowRoomID(%i)." % (self.id, self.avatarID, self.nowRoomID))
            return
        
        # 当前是否有操作
        if self._inOp():
            ERROR_MSG("Avatar(%i_%i):BExs_reqStartMatch but _inOp() = True." % (self.id, self.avatarID))
            return

        # 检查是否在匹配中
        if self._inMatch():
            ERROR_MSG("Avatar(%i_%i):BExs_reqStartMatch but _inMatch() = True." % (self.id, self.avatarID))
            return

        # 检查匹配类型是否合法
        if roomType not in GDefine.GC_RoomType.values():
            ERROR_MSG("Avatar(%i_%i):BExs_reqStartMatch roomType(%i) err." % (self.id, self.avatarID, roomType))
            return

        # 记录在操作中
        self._startOp(GDefine.GC_AvatarTime['startMatchOp'])

        # 通知大厅匹配房间
        self.nowHalls.B_reqMatchRoom(self, self.avatarID, roomType, {})

    def BExs_reqCancelMatch(self):
        """
        请求取消匹配
        """
        INFO_MSG("Avatar(%i_%i):BExs_reqCancelMatch." % (self.id, self.avatarID))
        
        # 当前是否有操作
        if self._inOp():
            ERROR_MSG("Avatar(%i_%i):BExs_reqCancelMatch but _inOp() = True." % (self.id, self.avatarID))
            return

        # 检查是否在匹配中
        if not self._inMatch():
            ERROR_MSG("Avatar(%i_%i):BExs_reqCancelMatch but _inMatch() = False." % (self.id, self.avatarID))
            return

        # 记录在操作中
        self._startOp(GDefine.GC_AvatarTime['cancelMatchOp'])

        # 通知大厅匹配房间
        self.nowHalls.B_reqCancelMatch(self, self.avatarID, self.roomType)