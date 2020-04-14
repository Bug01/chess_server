# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class room(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)

        self.cellData['cellRoomID'] = self.roomID
        self.cellData['cellRoomName'] = self.roomName
        self.cellData['cellMaxPlayerCount'] = self.maxPlayerCount
        self.cellData['cellGameID'] = self.gameID

        # 创建cell entity
        self.createCellEntityInNewSpace(None)
    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------
    def onGetCell(self):
        """
        这个函数在它获得cell实体的时候被调用。
        """
        INFO_MSG("%s(%i_%i):onGetCell." % (self.roomName, self.id, self.roomID))

        # 通知角色加入房间中
        for av in self.playerList:
            av['reqEnMB'].B_tellJoinRoom(self.cell, self.roomID, self.gameID)

    def onLoseCell(self):
        """
        这个函数在它关联的cell实体销毁之后被调用
        """
        INFO_MSG("%s(%i_%i):onLoseCell." % (self.roomName, self.id, self.roomID))

    
    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    
    # ---------------------------------------------------
    # 		Base method
    # ---------------------------------------------------
    
    
    