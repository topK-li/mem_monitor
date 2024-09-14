import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
import datetime
import os
import numpy as np

# 手动添加字体路径
font_path = '/usr/share/fonts/truetype/simhei/SimHei.ttf'
font_prop = fm.FontProperties(fname=font_path)

# 设置 Matplotlib 字体以支持中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 日志文件
log_file = "check.log"
img_dir = "img"

# 创建图像保存目录（如果不存在）
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

def parse_log_data(start_time, end_time):
    """
    解析日志文件并返回指定时间段内的进程数据，按PID分类。
    """
    processes = {}
    
    with open(log_file, "r") as f:
        current_time = None
        for line in f:
            if line.startswith("监控时间:"):
                current_time = datetime.datetime.strptime(line.split("监控时间: ")[1].strip(), "%Y-%m-%d %H:%M:%S")
                if current_time < start_time or current_time > end_time:
                    current_time = None
            elif current_time and line.strip() and not line.startswith("PID"):
                parts = line.split()
                pid = parts[0]
                user = parts[1]
                cpu = float(parts[2])
                mem = float(parts[3])
                command = parts[4]
                file_path = parts[5] if len(parts) > 5 else "N/A"

                if pid not in processes:
                    processes[pid] = {'timestamps': [], 'memory_usage': [], 'command': command, 'file_path': file_path}
                
                processes[pid]['timestamps'].append(current_time)
                processes[pid]['memory_usage'].append(mem)
    return processes

def filter_data(timestamps, memory_usages, max_points=100):
    """
    过滤内存使用情况数据，只在未变化时保留起始和结束点，在变化时智能选取采样点。
    """
    # 如果内存使用没有变化，只保留起始和结束点
    if len(set(memory_usages)) == 1:
        return [timestamps[0], timestamps[-1]], [memory_usages[0], memory_usages[-1]]

    # 如果内存使用发生变化，执行智能采样
    if len(timestamps) <= max_points:
        return timestamps, memory_usages

    # 初步筛选内存使用变化的点和起止点
    filtered_timestamps = [timestamps[0]]
    filtered_memory_usages = [memory_usages[0]]

    for i in range(1, len(memory_usages) - 1):
        if memory_usages[i] != memory_usages[i - 1] or memory_usages[i] != memory_usages[i + 1]:
            filtered_timestamps.append(timestamps[i])
            filtered_memory_usages.append(memory_usages[i])

    filtered_timestamps.append(timestamps[-1])
    filtered_memory_usages.append(memory_usages[-1])
    
    # 如果过滤后的点数仍然超过限制，则进行智能采样
    if len(filtered_timestamps) > max_points:
        interval = len(filtered_timestamps) // max_points
        sampled_timestamps = []
        sampled_memory_usages = []
        for i in range(0, len(filtered_timestamps), interval):
            end = min(i + interval, len(filtered_timestamps))
            segment = filtered_memory_usages[i:end]
            max_index = np.argmax(segment)
            sampled_timestamps.append(filtered_timestamps[i + max_index])
            sampled_memory_usages.append(filtered_memory_usages[i + max_index])
        return sampled_timestamps, sampled_memory_usages
    
    return filtered_timestamps, filtered_memory_usages

def plot_memory_usage(processes, title, start_time, end_time):
    """
    绘制内存使用情况的折线图，每个PID单独生成图表。
    """
    for pid, data in processes.items():
        if data['timestamps'] and data['memory_usage']:
            timestamps = data['timestamps']
            memory_usages = data['memory_usage']
            command = data['command']
            file_path = data['file_path']

            # 过滤数据，智能选择采样点
            filtered_timestamps, filtered_memory_usages = filter_data(timestamps, memory_usages)

            plt.figure(figsize=(12, 6))
            plt.plot(filtered_timestamps, filtered_memory_usages, marker='o', linestyle='-', label=f"{command} ({file_path})")
            plt.title(f"{title} - PID: {pid}, Program: {command}", fontproperties=font_prop)
            plt.xlabel("时间", fontproperties=font_prop)
            plt.ylabel("内存使用率 (%)", fontproperties=font_prop)

            # 设置 x 轴格式化
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            plt.xticks(rotation=45, fontproperties=font_prop)
            
            plt.tight_layout()
            plt.grid(True)

            # 标注峰值
            max_memory_index = filtered_memory_usages.index(max(filtered_memory_usages))
            plt.annotate(f"{filtered_memory_usages[max_memory_index]:.2f}%", 
                         (filtered_timestamps[max_memory_index], filtered_memory_usages[max_memory_index]), 
                         textcoords="offset points", xytext=(0, 10), ha='center', fontproperties=font_prop)

            # 保存图像到 img 目录，文件名包含PID和时间跨度
            filename = f"memory_usage_{command}_{pid}_{start_time.strftime('%Y%m%d%H%M%S')}_{end_time.strftime('%Y%m%d%H%M%S')}.png"
            plt.savefig(os.path.join(img_dir, filename))
            plt.close()
            print(f"已生成并保存内存使用情况折线图：{filename}")

def get_time_range(option):
    """
    根据用户选项返回时间范围。
    """
    now = datetime.datetime.now()
    if option == '1':
        return now - datetime.timedelta(seconds=30), now
    elif option == '2':
        return now - datetime.timedelta(minutes=1), now
    elif option == '3':
        return now - datetime.timedelta(minutes=5), now
    elif option == '4':
        return now - datetime.timedelta(minutes=30), now
    elif option == '5':
        return now - datetime.timedelta(hours=1), now
    elif option == '6':
        return now - datetime.timedelta(hours=3), now
    elif option == '7':
        return now - datetime.timedelta(hours=6), now
    elif option == '8':
        return now - datetime.timedelta(hours=12), now
    elif option == '9':
        return now - datetime.timedelta(days=1), now
    elif option == '10':
        start_str, end_str = input("请输入时间范围 (格式: YYYYMMDDHHMMSS-YYYYMMDDHHMMSS): ").split('-')
        start_time = datetime.datetime.strptime(start_str, "%Y%m%d%H%M%S")
        end_time = datetime.datetime.strptime(end_str, "%Y%m%d%H%M%S")
        return start_time, end_time
    else:
        print("无效选项，请重新选择。")
        return None, None

if __name__ == "__main__":
    print("请选择生成图表的时间范围：")
    print("1: 最近30秒")
    print("2: 最近1分钟")
    print("3: 最近5分钟")
    print("4: 最近30分钟")
    print("5: 最近1小时")
    print("6: 最近3小时")
    print("7: 最近6小时")
    print("8: 最近12小时")
    print("9: 最近24小时")
    print("10: 用户自选时间段")

    option = input("请输入选项编号: ")
    start_time, end_time = get_time_range(option)

    if start_time and end_time:
        processes = parse_log_data(start_time, end_time)
        plot_memory_usage(processes, f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%Y-%m-%d %H:%M:%S')}", start_time, end_time)

