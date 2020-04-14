# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from halls import halls

class gobangHalls(halls):
    def __init__(self):
        halls.__init__(self)

        self.gameID = 10

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------

    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def _createRoom(self, roomType, avList):
        """
        创建房间
        参数1：房间类型
        参数2：房间内玩家列表
        """
        param = {
                # 大厅信息
                'masterHalls'		: self,
                'masterHallsName'	: self.hallsName,

                # 房间基本属性
                'roomID'			: 100000,
                'roomType'			: roomType,
                'roomName'			: 'gobangRoom',
                'gameID'			: self.gameID,

                # 房间内玩家
                'maxPlayerCount'	: 2,
                'playerList'		: avList,
        }
        KBEngine.createEntityAnywhere('gobangRoom', param)
    
    # ---------------------------------------------------
    # 		Base 接口
    # ---------------------------------------------------
    
    
    