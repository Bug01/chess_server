#!/bin/sh

currPath=$(pwd)
keyStr="/kbengine/"

bcontain=`echo $currPath|grep $keyStr|wc -l`


if [ $bcontain = 0 ]
then
	export KBE_ROOT="$(cd ../; pwd)"
else
	export KBE_ROOT="$(pwd | awk -F "/kbengine/" '{print $1}')/kbengine"
fi



export KBE_RES_PATH="$KBE_ROOT/kbe/res/:$(pwd):$(pwd)/res:$(pwd)/scripts/"
export KBE_BIN_PATH="$KBE_ROOT/kbe/bin/server/"

echo KBE_ROOT = \"${KBE_ROOT}\"
echo KBE_RES_PATH = \"${KBE_RES_PATH}\"
echo KBE_BIN_PATH = \"${KBE_BIN_PATH}\"

sh ./kill_server.sh

"$KBE_BIN_PATH/machine" --cid=1000 --gus=1000&
"$KBE_BIN_PATH/logger" --cid=2000 --gus=2000&
"$KBE_BIN_PATH/interfaces" --cid=3000 --gus=3000&
"$KBE_BIN_PATH/dbmgr" --cid=4000 --gus=4000&
"$KBE_BIN_PATH/baseappmgr" --cid=5000 --gus=5000&
"$KBE_BIN_PATH/cellappmgr" --cid=6000 --gus=6000&
"$KBE_BIN_PATH/baseapp" --cid=7001 --gus=7001&
"$KBE_BIN_PATH/baseapp" --cid=7002 --gus=7002&
"$KBE_BIN_PATH/cellapp" --cid=8001 --gus=8001&
"$KBE_BIN_PATH/cellapp" --cid=8002 --gus=8002&
"$KBE_BIN_PATH/loginapp" --cid=9000 --gus=9000&
