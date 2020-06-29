# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from room import room

class gobangRoom(room):
    def __init__(self):
        room.__init__(self)

        # 棋盘数组
        self.table = []
        self.maxPos = 15
        self.freeCount = 0

        # 当前回合数
        self.curRound = 0

        # 当前申请和棋的角色
        self.curDrawChairID = 0

        # 当前申请悔棋的位置
        self.curBackChaidID = 0

    # ---------------------------------------------------
    # 		KBEngine method
    # ---------------------------------------------------

    # ---------------------------------------------------
    # 		Default method
    # ---------------------------------------------------
    def _tellAllAVStart(self):
        """
        通知开始游戏
        """
        # 通知开始游戏
        for av in self.cellAvatars.values():
            if av.getOnline():
                av.base.client.Exs_onStartGame()
    
    def _tellAllAVCurPlayer(self):
        """
        通知当然下子玩家
        """
        # 通知当前玩家
        for av in self.cellAvatars.values():
            if av.getOnline():
                av.base.client.Exs_tellCurPlayer(self.curRound, self.curChairID)

    def _tellAllAVChess(self, pos_x, pos_y):
        """
        通知下子位置
        参数1：下子位置x
        参数2：下子位置y
        """
        # 通知下子位置
        for av in self.cellAvatars.values():
            if av.getOnline():
                av.base.client.Exs_tellPlayerChess(self.curChairID, pos_x, pos_y)

    def _tellAllAVConsent(self, chairID, tp):
        """
        通知请求对方同意
        参数1：请求位置
        参数2：请求类型
                1：和棋
                2：悔棋
                3：认输
        """
        for av in self.cellAvatars.values():
            if av.getOnline():
                av.base.client.Exs_tellPlayerConsent(chairID, tp)

    def _tellAllAVConsentBack(self, chairID, tp, bAgree):
        """
        通知请求对方同意
        参数1：请求位置
        参数2：请求类型
                1：和棋
                2：悔棋
                3：认输
        参数3：是否同意
        """
        for av in self.cellAvatars.values():
            if av.getOnline():
                av.base.client.Exs_tellPlayerConsentBack(chairID, tp, bAgree)


    def _tellAllAVEnd(self, winPos):
        """
        通知游戏结束
        """
        # 通知游戏结束
        for av in self.cellAvatars.values():
            if av.getOnline():
                av.base.client.Exs_onEndGame(winPos)

    def _checkFiveInLine(self, pos_x, pos_y, tarVal):
        """
        检查五子连线
        参数1：当前下子的位置x
        参数2：当前下子的位置y
        参数3：当前下子的棋子颜色
        """
        # 检查横向
        count = 1
        t_x = pos_x + 1
        while t_x < self.maxPos and self.table[t_x][pos_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_x += 1

        t_x = pos_x - 1
        while t_x >= 0 and self.table[t_x][pos_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_x -= 1

        # 检查纵向
        count = 1
        t_y = pos_y + 1
        while t_y < self.maxPos and self.table[pos_x][t_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_y += 1

        t_y = pos_y - 1
        while t_y >= 0 and self.table[pos_x][t_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_y -= 1

        # 左下到右上斜向
        count = 1
        t_x = pos_x - 1
        t_y = pos_y - 1
        while t_x >= 0 and t_y >= 0 and self.table[t_x][t_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_x -= 1
            t_y -= 1

        t_x = pos_x + 1
        t_y = pos_y + 1
        while t_x < self.maxPos and t_y < self.maxPos and self.table[t_x][t_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_x += 1
            t_y += 1

        # 右下到左上斜向
        count = 1
        t_x = pos_x + 1
        t_y = pos_y - 1
        while t_x < self.maxPos and t_y >= 0 and self.table[t_x][t_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_x += 1
            t_y -= 1

        t_x = pos_x - 1
        t_y = pos_y + 1
        while t_x < self.maxPos and t_y < self.maxPos and self.table[t_x][t_y] == tarVal:
            count += 1
            if count >= 5:
                return True
            t_x -= 1
            t_y += 1

        return False

    def onTimeout(self):
        """
        """
        # 超时算认输
        self.curChairID = self.curChairID % self.cellMaxPlayerCount + 1
        self.onEndGame(self.curChairID)

    def onStartGame(self):
        """
        开始游戏
        """
        # 房间开始游戏
        room.onStartGame(self)

        # 确定开始位置
        self.curChairID = 0
        self.table = [[0 for i in range(self.maxPos)] for j in range(self.maxPos)]
        self.freeCount = self.maxPos * self.maxPos

        # 通知开始游戏
        self._tellAllAVStart()

        # 开始游戏循环
        self.onRound()

    def onRound(self):
        """
        进行游戏回合
        """
        self.curChairID = self.curChairID % self.cellMaxPlayerCount + 1
        self.curRound += 1

        # 启动一个定时器
        self.resetTimer(30)

        # 通知下子
        self._tellAllAVCurPlayer()

    def reqChess(self, reqDBID, reqCellEnMB, pos_x, pos_y):
        """
        通知下子
        参数1：角色的DBID
        参数2：角色的cellCall
        参数3：下子位置x
        参数4：下子位置y
        """
        # 检查在游戏中
        if not self.inGame():
            ERROR_MSG("%s(%i)reqChess:reqDBID(%i) but not in game." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 检查是否该我
        if self.curChairID != reqCellEnMB.getChairID():
            ERROR_MSG("%s(%i)reqChess:ChairID(%i) but curChairID(%i)." \
                % (self.cellRoomName, self.cellRoomID, reqCellEnMB.getChairID(), self.curChairID))
            return

        # 检查位置是否合法
        if pos_x > self.maxPos or pos_y > self.maxPos:
            ERROR_MSG("%s(%i)reqChess:reqDBID(%i) but pos_x(%i) pos_y(%i) err." \
                % (self.cellRoomName, self.cellRoomID, reqDBID, pos_x, pos_y))
            return

        # 该位置是否是空位置
        if self.table[pos_x][pos_y] != 0:
            ERROR_MSG("%s(%i)reqChess:reqDBID(%i) but table[%i][%i]=%i not 0." \
                % (self.cellRoomName, self.cellRoomID, reqDBID, pos_x, pos_y, self.table[pos_x][pos_y]))
            return

        # 下子
        self.table[pos_x][pos_y] = reqCellEnMB.getChairID()
        self.freeCount -= 1
        self.curBackChaidID = 0

        # 最后落子
        reqCellEnMB.lastChessPos(pos_x, pos_y)

        # 通知下子位置
        self._tellAllAVChess(pos_x, pos_y)

        # 检擦游戏是否结束
        if self._checkFiveInLine(pos_x, pos_y, reqCellEnMB.getChairID()):
            self.onEndGame(reqCellEnMB.getChairID())
            return

        # 检查是否放满和棋子
        if self.freeCount == 0:
            self.onEndGame(0)
            return

        # 继续游戏
        self.onRound()

    def reqDraw(self, reqDBID, reqCellEnMB, tp):
        """
        请求和棋
        参数1：角色的DBID
        参数2：角色的cellCall
        参数3：请求和棋
        """
        # 检查在游戏中
        if not self.inGame():
            ERROR_MSG("%s(%i)reqDraw:reqDBID(%i) but not in game." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 已经申请了和棋
        if self.curDrawChairID != 0:
            ERROR_MSG("%s(%i)reqDraw:reqDBID(%i) but is curDrawChairID." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 申请和棋
        self.curDrawChairID = reqCellEnMB.getChairID()

        # 通知下去
        self._tellAllAVConsent(reqCellEnMB.getChairID(), tp)
        

    def reqDrawBack(self, reqDBID, reqCellEnMB, tp, bAgree):
        """
        请求回应对方是否同意
        参数1：角色的DBID
        参数2：角色的cellCall
        参数3：请求和棋
        参数4：是否同意和棋
        """
        # 检查在游戏中
        if not self.inGame():
            ERROR_MSG("%s(%i)reqDrawBack:reqDBID(%i) but not in game." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 没人申请了和棋或者是我申请的 所以不用同意
        if self.curDrawChairID == 0 or self.curDrawChairID == reqCellEnMB.getChairID():
            ERROR_MSG("%s(%i)reqDrawBack:reqDBID(%i) but curDrawChairID is None." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 通知下去
        self._tellAllAVConsentBack(reqCellEnMB.getChairID(), tp, bAgree)

        # 同意和棋
        if bAgree:
            self.onEndGame(0)
            return

        # 不同意
        else:
            self.curDrawChairID = 0

    def reqBackChess(self, reqDBID, reqCellEnMB, tp):
        """
        请求悔棋
        参数1：角色的DBID
        参数2：角色的cellCall
        参数3：请求悔棋
        """
        # 检查在游戏中
        if not self.inGame():
            ERROR_MSG("%s(%i)reqBackChess:reqDBID(%i) but not in game." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 当前轮我操作 不能申请
        if self.curChairID == reqCellEnMB.getChairID():
            ERROR_MSG("%s(%i)reqBackChess:reqDBID(%i) but curChairID is me." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 已经申请悔棋
        if self.curBackChaidID != 0:
            ERROR_MSG("%s(%i)reqBackChess:reqDBID(%i) but has req." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 通知悔棋消息
        self._tellAllAVConsent(reqCellEnMB.getChairID(), tp)

        # 申请悔棋
        self.curBackChaidID = reqCellEnMB.getChairID()

    def reqBackChessBack(self, reqDBID, reqCellEnMB, tp, bAgree):
        """
        请求回应对方是否同意
        参数1：角色的DBID
        参数2：角色的cellCall
        参数3：回应类型
                1：和棋
                2：悔棋
                3：认输
        参数4：是否同意
        """
        # 检查在游戏中
        if not self.inGame():
            ERROR_MSG("%s(%i)reqBackChessBack:reqDBID(%i) but not in game." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 如果当前没人申请悔棋或者是我申请的悔棋 不能同意或不同意
        if self.curBackChaidID == 0 or self.curBackChaidID == reqCellEnMB.getChairID():
            ERROR_MSG("%s(%i)reqBackChessBack:reqDBID(%i) but no player back." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 通知悔棋消息
        self._tellAllAVConsentBack(reqCellEnMB.getChairID(), tp, bAgree)

        # 同意悔棋
        if bAgree:
            # 撤回落子
            lastAV = self.curChairID % self.cellMaxPlayerCount + 1
            self.table[lastAV.lastPos_x][lastAV.lastPos_y] = 0
            self.freeCount += 1
            lastAV.clearLastChess()
            
            # 通知撤回落子
            # .......

            # 继续游戏
            self.onRound()
        # 拒绝悔棋
        else:
            self.curBackChaidID = 0

    def reqLose(self, reqDBID, reqCellEnMB):
        """
        请求认输
        参数1：角色的DBID
        参数2：角色的cellCall
        """
        # 检查在游戏中
        if not self.inGame():
            ERROR_MSG("%s(%i)reqLose:reqDBID(%i) but not in game." % (self.cellRoomName, self.cellRoomID, reqDBID))
            return

        # 游戏结束
        for dbid in self.cellAvatars:
            if dbid != reqDBID:
                self.onEndGame(dbid)    
                return

    def onEndGame(self, winPos):
        """
        结束游戏
        参数1：赢家位置
        """
        # 房间结束游戏
        room.onEndGame(self, winPos)

        # 通知游戏结束
        self._tellAllAVEnd(winPos)

        # 销毁房间
        self.destroyRoom()
    # ---------------------------------------------------
    # 		Base 接口
    # ---------------------------------------------------
    
    
    