# -*- coding: utf-8 -*-

# 服务实体
GC_ServerEntity = {
	
	'mainHalls' : { 
		'cid' 			: '7000',
		'bOpen'			: True,
		'bLoadBalance'	: True, 
		'default' 		: {
			'entityName' 	: 'mainHalls',
		}
	},

	'chessHalls' : {
		'cid'			: '7000',
		'bOpen'			: True,
		'bLoadBalance'	: True,
		'default'		: {
			'hallsName'	: 'chessHalls',
		}
	},

	'gobangHalls' : {
		'cid'			: '7000',
		'bOpen'			: True,
		'bLoadBalance'	: True,
		'default'		: {
			'hallsName'	: 'gobangHalls',
		}
	},
}

# 服务器ID对应的游戏大厅
GC_ServerIDToHalls = {
	1 : 'chessHalls',
	2 : 'gobangHalls',
}

# appID信息
GC_APPInfo = {
	'appID'		: 'wx4836c6125853dbf7',
	'AppSecret' : 'f06fdf1bd4d0ca5493e59233153686a2',
}