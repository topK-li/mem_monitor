import psutil
import time
from datetime import datetime

def log_top_processes():
    """
    记录内存使用前20的进程的CPU、内存使用情况、可执行文件路径和命令行参数到控制台。
    """
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 打印时间戳到控制台
    print(f"监控时间: {current_time}")
    print("PID\tUSER\t%CPU\t%MEM\tCOMMAND\tFILE_PATH\tCMDLINE")

    # 获取所有进程的信息
    processes = []
    for proc in psutil.process_iter(['pid', 'username', 'cpu_percent', 'memory_percent', 'name', 'exe', 'cmdline']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # 按内存使用情况排序，取前20名
    top_processes = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)[:20]

    # 将进程信息打印到控制台
    for proc in top_processes:
        pid = proc['pid']
        user = proc['username']
        cpu = proc['cpu_percent']
        mem = proc['memory_percent']
        command = proc['name']
        file_path = proc['exe'] if proc['exe'] else "N/A"  # 如果无法访问文件路径，则使用 "N/A"
        cmdline = ' '.join(proc['cmdline']) if proc['cmdline'] else "N/A"  # 如果无法访问命令行参数，则使用 "N/A"
        
        print(f"{pid}\t{user}\t{cpu:.2f}\t{mem:.2f}\t{command}\t{file_path}\t{cmdline}")

    print("\n")

def monitor_processes():
    """
    持续监控进程并每秒记录数据。
    """
    while True:
        log_top_processes()
        time.sleep(1)

if __name__ == "__main__":
    monitor_processes()
