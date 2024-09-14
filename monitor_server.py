import psutil
import time
from datetime import datetime

def log_memory_usage():
    """
    记录服务器的整体内存使用情况到控制台。
    """
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 获取整体内存使用情况
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 * 1024)  # 转换为 MB
    used_memory = memory_info.used / (1024 * 1024)  # 转换为 MB
    percent_memory = memory_info.percent

    # 打印内存使用情况到控制台
    print(f"监控时间: {current_time}")
    print(f"总内存: {total_memory:.2f} MB, 已用内存: {used_memory:.2f} MB, 使用率: {percent_memory:.2f}%")
    print("\n")

def monitor_memory():
    """
    持续监控服务器的整体内存使用情况。
    """
    while True:
        log_memory_usage()
        time.sleep(1)

if __name__ == "__main__":
    monitor_memory()
