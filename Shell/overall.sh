#!/bin/bash

# 定义本地变量
arg="$1"

# 脚本帮助信息
usage(){
    echo "脚本$0的使用方式是：$0 [start|stop|restart ]"
}

# 函数的主框架
if [ $# -eq 1 ]
then
    case "${arg}" in
        start)
            echo "服务启动中"
        ;;
        stop)
            echo "服务关闭中"
        ;;
    restart)
        echo "服务重启中"
        ;;
    *)
        usage
        ;;
    esac
else
    usage
fi

