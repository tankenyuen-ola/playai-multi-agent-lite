#!/bin/bash

# 设置环境变量
export PYTHONPATH=$(pwd)

# 定义 PID 文件路径
PID_FILE="gunicorn.pid"
LOG_DIR="logs"

# 确保日志目录存在
mkdir -p $LOG_DIR

# 获取 Gunicorn 进程 PID
get_pid() {
    if [ -f $PID_FILE ]; then
        cat $PID_FILE
    fi
}

# 检查服务是否在运行
is_running() {
    pid=$(get_pid)
    if [ -n "$pid" ]; then
        if ps -p $pid > /dev/null 2>&1; then
            return 0  # 正在运行
        fi
    fi
    return 1  # 没有运行
}

# 启动服务
start() {
    echo "Starting server..."
    if is_running; then
        echo "Server is already running."
        exit 1
    fi
    
    # 使用 gunicorn 启动服务，并将 PID 写入文件
    gunicorn main:app \
        -c gunicorn_config.py \
        --pid $PID_FILE \
        --daemon
    
    # 等待几秒检查是否成功启动
    sleep 2
    if is_running; then
        echo "Server started successfully."
    else
        echo "Failed to start server."
        exit 1
    fi
}

# 停止服务
stop() {
    echo "Stopping server..."
    pid=$(get_pid)
    if [ -n "$pid" ]; then
        # 首先尝试优雅停止
        kill -TERM $pid
        
        # 等待进程结束
        for i in {1..10}; do
            if ! is_running; then
                break
            fi
            sleep 1
        done
        
        # 如果进程仍在运行，强制终止
        if is_running; then
            echo "Force stopping server..."
            kill -9 $pid
        fi
        
        rm -f $PID_FILE
        echo "Server stopped."
    else
        echo "Server is not running."
    fi
}

# 重启服务
restart() {
    echo "Restarting server..."
    stop
    sleep 2
    start
}

# 检查服务状态
status() {
    if is_running; then
        pid=$(get_pid)
        echo "Server is running (PID: $pid)"
    else
        echo "Server is not running"
    fi
}

# 主命令处理
case "$1" in
    "start")
        start
        ;;
    "stop")
        stop
        ;;
    "restart")
        restart
        ;;
    "status")
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
