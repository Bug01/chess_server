# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GDataTmp
import GTools

class Account(KBEngine.Proxy):
    def __init__(self):
        KBEngine.Proxy.__init__(self)

        # 当前角色
        self.curAvatar = None

        # 登陆时客户端的数据
        self.clientData = GTools.json_load(self.getClientDatas()[0])
        
    # ---------------------------------------------------
    # 				KBEngine method
    # ---------------------------------------------------
    def onTimer(self, id, userArg):
        """
        KBEngine method.
        使用addTimer后， 当时间到达则该接口被调用
        @param id		: addTimer 的返回值ID
        @param userArg	: addTimer 最后一个参数所给入的数据
        """
        DEBUG_MSG("Account(%i):onTimer. id(%s) userArg(%s)." % (self.id, tid, userArg))
        
    def onClientEnabled(self):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        INFO_MSG("Account(%i) entities enable." % (self.id))

        # 更新最后登陆时间
        self.lastReloginTime = GTools.nowTime()
            
    def onLogOnAttempt(self, ip, port, password):
        """
        KBEngine method.
        客户端登陆失败时会回调到这里
        """
        return KBEngine.LOG_ON_ACCEPT
        
    def onClientDeath(self):
        """
        KBEngine method.
        客户端对应实体已经销毁
        """
        DEBUG_MSG("Account(%i) onClientDeath." % (self.id))
        # self.destroy()

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        DEBUG_MSG("Account(%i) onDestroy." % (self.id))
        
        # 解除与角色的引用
        if self.curAvatar:
            self.curAvatar.accountEntity = None
            self.curAvatar = None

    # ---------------------------------------------------
    # 				Default method
    # ---------------------------------------------------
    def _onAvatarSaved(self, bSuccess, newAV):
        """
        角色实体存库后的回调
        参数1：成功或失败
        参数2：base实体
        """
        # 如果创建过程中账号已经销毁
        if self.isDestroyed and newAV:
            newAV.destroy(True)
            return

        if bSuccess:
            # 保存实体的唯一ID
            newAV.avatarID = newAV.databaseID

            # 记录到列表
            props = GTools.dcopy(GDataTmp.Avatar_Info_In_Account)
            props['avatarID'] = newAV.avatarID
            props['serverID'] = newAV.serverID
            self.avatarDict[newAV.serverID] = props
            self.writeToDB()

            # 销毁实体
            newAV.destroy()

        # 通知创建结果
        if self.client is not None:
            self.client.Exs_ackCreateAvatar(bSuccess, props)

    def _onAvatarCreated(self, baseRef, databaseID, wasActive):
        """
        从数据库加载创建角色回调
        如果操作失败，baseRef将会是None，databaseID将会是0，wasActive将会是False
        参数1：新创建实体的引用或者已经存在的实体的EntityCall
        参数2：实体的数据库ID
        参数3：实体是否已经激活 如果为true 则参数1表示实体的EntityCall
        """
        if wasActive:
            ERROR_MSG("Account::_onAvatarCreated:(%i): the avatar has in the world." % (self.id))
            return
        if baseRef is None:
            ERROR_MSG("Account::_onAvatarCreated:(%i): avatar create failed." % (self.id))
            return
        
        # 获取实体
        avatar = KBEngine.entities.get(baseRef.id)
        if avatar is None:
            ERROR_MSG("Account::_onAvatarCreated:(%i): the avatar has destroy." % (self.id))
            return

        if self.isDestroyed:
            ERROR_MSG("Account::_onAvatarCreated:(%i): the account has destroy." % (self.id))
            avatar.destroy()
            return

        # 控制权交给avatar
        avatar.accountEntity = self
        self.curAvatar = avatar
        self.giveClientTo(avatar)

    # ---------------------------------------------------
    # 				BExs method
    # ---------------------------------------------------
    def BExs_reqAvatarList(self):
        """
        请求角色列表
        """
        # 返回角色列表
        if self.client is not None:
            ret = list(self.avatarDict.values())
            self.client.Exs_ackAvatarList(ret, self.lastServerID)

    def BExs_reqCreateAvatar(self, serverID):
        """
        请求创建角色
        参数1：服务器ID
        """
        INFO_MSG("Account(%i). BExs_reqCreateAvatar serverID(%s)." % (self.id, serverID))

        # 已经存在
        if serverID in self.avatarDict:
            ERROR_MSG("Account(%i). BExs_reqCreateAvatar serverID(%i) has existe." % (self.id, serverID))
            return

        # 本地创建实体
        props = {
            'avatarID'		: 0,
            'serverID'		: serverID,
        }
        newAV = KBEngine.createEntityLocally('Avatar', props)

        # 创建后立即保存获取databaseID
        if newAV:
            newAV.writeToDB(self._onAvatarSaved)

    def BExs_reqEnterGame(self, serverID):
        """
        选择角色进入游戏
        参数1：选择的服务器ID
        """
        if self.curAvatar is None:
            if serverID in self.avatarDict:
                self.lastServerID = serverID
                avatarID = self.avatarDict[serverID]['avatarID']

                # 角色存在则从数据库创建
                KBEngine.createEntityFromDBID('Avatar', avatarID, self._onAvatarCreated)
            else:
                ERROR_MSG("Account(%i)::BExs_reqEnterGame: not found serverID(%i)." % (self.id, serverID))
        else:
            # 控制权交给avatar
            self.giveClientTo(self.curAvatar)