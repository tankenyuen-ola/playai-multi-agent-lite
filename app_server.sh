#!/bin/bash

# 应用配置
APP_NAME="playai-multi-agent"
#APP_DIR="/opt/playai-multi-agent"  # 生产环境目录
APP_DIR="/home/kenyuen/playai-multi-agent-lite"
USER="www-data"                    # Ubuntu 默认 web 服务用户
GROUP="www-data"                   # Ubuntu 默认 web 服务用户组

# 运行时配置
WORKERS=4                          # worker 进程数，可以根据 CPU 核心数调整
PORT=8000                         # 应用端口
#BIND="0.0.0.0:$PORT"             # 绑定地址
BIND="127.0.0.1:$PORT"
TIMEOUT=120                       # 超时时间

# 目录配置
LOG_DIR="/var/log/$APP_NAME"      # Ubuntu 标准日志目录
PID_DIR="/var/run/$APP_NAME"      # Ubuntu 标准 PID 目录
VENV_DIR="$APP_DIR/.venv"          # 虚拟环境目录
#VENV_DIR="/home/banban/.local/bin/poetry"

# 文件路径
PID_FILE="$PID_DIR/$APP_NAME.pid"
ACCESS_LOG="$LOG_DIR/access.log"
ERROR_LOG="$LOG_DIR/error.log"
GUNICORN_CONFIG="$APP_DIR/gunicorn_config.py"

# 确保目录存在并设置正确的权限
setup_directories() {
    # 创建必要的目录
    for DIR in "$LOG_DIR" "$PID_DIR"; do
        if [ ! -d "$DIR" ]; then
            sudo mkdir -p "$DIR"
            sudo chown -R $USER:$GROUP "$DIR"
            sudo chmod 755 "$DIR"
        fi
    done
}

# 获取进程 PID
get_pid() {
    if [ -f "$PID_FILE" ]; then
        cat "$PID_FILE"
    fi
}

# 检查服务是否在运行
is_running() {
    pid=$(get_pid)
    if [ -n "$pid" ]; then
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # 正在运行
        fi
    fi
    return 1  # 没有运行
}

# 激活虚拟环境
activate_venv() {
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
    else
        echo "Virtual environment not found at $VENV_DIR"
        exit 1
    fi
}

# 启动服务
start() {
    echo "Starting $APP_NAME..."
    
    # 检查是否已经在运行
    if is_running; then
        echo "$APP_NAME is already running."
        exit 1
    fi
    
    # 设置目录
    setup_directories
    
    # 激活虚拟环境
    activate_venv
    
    # 启动 Gunicorn
    #sudo -u $USER gunicorn main:app \
    #python /home/kenyuen/playai-multi-agent-lite/.venv/bin/gunicorn main:app \
    /home/kenyuen/playai-multi-agent-lite/.venv/bin/gunicorn main:app \
    #gunicorn main:app \
        --name $APP_NAME \
        --workers $WORKERS \
        --bind $BIND \
        --timeout $TIMEOUT \
        --pid $PID_FILE \
        --user $USER \
        --group $GROUP \
        --daemon \
        --worker-class uvicorn.workers.UvicornWorker \
        --access-logfile $ACCESS_LOG \
        --error-logfile $ERROR_LOG \
        --capture-output \
        --log-level info
    
    # 检查启动状态
    sleep 2
    if is_running; then
        echo "$APP_NAME started successfully"
    else
        echo "Failed to start $APP_NAME"
        exit 1
    fi
}

# 停止服务
stop() {
    echo "Stopping $APP_NAME..."
    pid=$(get_pid)
    if [ -n "$pid" ]; then
        # 尝试优雅停止
        sudo kill -TERM "$pid"
        
        # 等待进程结束
        for i in {1..30}; do
            if ! is_running; then
                break
            fi
            echo "Waiting for $APP_NAME to stop... ($i/30)"
            sleep 1
        done
        
        # 如果还在运行，强制终止
        if is_running; then
            echo "Force stopping $APP_NAME..."
            sudo kill -9 "$pid"
        fi
        
        sudo rm -f "$PID_FILE"
        echo "$APP_NAME stopped"
    else
        echo "$APP_NAME is not running"
    fi
}

# 重启服务
restart() {
    echo "Restarting $APP_NAME..."
    stop
    sleep 2
    start
}

# 检查状态
status() {
    if is_running; then
        pid=$(get_pid)
        echo "$APP_NAME is running (PID: $pid)"
        echo "Logs are available at:"
        echo "  Access log: $ACCESS_LOG"
        echo "  Error log: $ERROR_LOG"
    else
        echo "$APP_NAME is not running"
    fi
}

# 检查系统资源
check_resources() {
    echo "System Resources for $APP_NAME:"
    echo "CPU Usage:"
    if is_running; then
        pid=$(get_pid)
        ps -p "$pid" -o %cpu,%mem,cmd
        echo -e "\nMemory Usage:"
        free -h
        echo -e "\nDisk Usage:"
        df -h "$LOG_DIR"
    else
        echo "$APP_NAME is not running"
    fi
}

# 查看日志
view_logs() {
    case "$1" in
        "access")
            sudo tail -f "$ACCESS_LOG"
            ;;
        "error")
            sudo tail -f "$ERROR_LOG"
            ;;
        *)
            echo "Usage: $0 logs {access|error}"
            exit 1
            ;;
    esac
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
    "resources")
        check_resources
        ;;
    "logs")
        view_logs "$2"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|resources|logs}"
        echo "For logs: $0 logs {access|error}"
        exit 1
        ;;
esac

exit 0
