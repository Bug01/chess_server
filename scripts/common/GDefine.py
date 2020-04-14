# -*- coding: utf-8 -*-

# 角色的定时器(initialOffset, repeatOffset, userArg)
# 注意 userArg 不要相同
GC_AvatarTime = {
    'startMatchOp' : {
        'initialOffset'	: 10,		# 10s后开始执行
        'repeatOffset'	: 0,		# 不循环
        'userArg'		: 101,		# 开始匹配操作
    },
    'cancelMatchOp' : {
        'initialOffset'	: 10,		# 10s后开始执行
        'repeatOffset'	: 0,		# 不循环
        'userArg'		: 102,		# 取消匹配操作
    },
}

# 大厅中定时器 (initialOffset, repeatOffset, userArg)
# 注意 userArg 不要相同
GC_HallsTime = {
    'regToMainHalls' : {
        'initialOffset'	: 1,		# 1s后开始执行
        'repeatOffset'	: 1,		# 每1s循环一次
        'userArg'		: 201,		# 携带的参数
    },
}

# 匹配服务中定时器 (initialOffset, repeatOffset, userArg)
# 注意 userArg 不要相同
GC_MatchTime = {
    'matchInterval' : {
        'initialOffset'	: 2,		# 2s后开始执行
        'repeatOffset'	: 2,		# 每2s循环一次
        'userArg'		: 301,		# 携带的参数
    },
}


# 房间类型
GC_RoomType = {
    'Create'	: 0,		# 自建房
    'Robot'		: 1,		# 人机赛匹配
    'Match'		: 2,		# 匹配赛匹配
    'Rank'		: 3,		# 排位赛匹配
}

# 房间状态
GC_RoomStatus = {
    'free'		: 0,		# 空闲
    'game'		: 1,		# 游戏中
    'end'		: 2,		# 游戏结束
}