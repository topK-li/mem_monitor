import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
import datetime
import os

# 手动添加字体路径
font_path = '/usr/share/fonts/truetype/simhei/SimHei.ttf'
font_prop = fm.FontProperties(fname=font_path)

# 设置 Matplotlib 字体以支持中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 日志文件
log_file = "server_memory.log"
img_dir = "img"

# 创建图像保存目录（如果不存在）
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

def parse_log_data(start_time, end_time):
    """
    解析日志文件并返回指定时间段内的内存使用情况数据。
    """
    timestamps = []
    memory_usages = []
    
    with open(log_file, "r") as f:
        current_time = None
        for line in f:
            if line.startswith("监控时间:"):
                current_time = datetime.datetime.strptime(line.split("监控时间: ")[1].strip(), "%Y-%m-%d %H:%M:%S")
                if current_time < start_time or current_time > end_time:
                    current_time = None
                else:
                    timestamps.append(current_time)
            elif current_time and line.strip().startswith("总内存:"):
                parts = line.split(",")
                mem_percent = float(parts[2].split(":")[1].strip().replace('%', ''))
                memory_usages.append(mem_percent)
    return timestamps, memory_usages

def plot_memory_usage(timestamps, memory_usages, title):
    """
    绘制整体内存使用情况的折线图。
    """
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, memory_usages, marker='o', linestyle='-', label="Memory Usage")
    plt.title(f"{title}", fontproperties=font_prop)
    plt.xlabel("时间", fontproperties=font_prop)
    plt.ylabel("内存使用率 (%)", fontproperties=font_prop)

    # 设置 x 轴格式化
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.xticks(rotation=45, fontproperties=font_prop)

    plt.tight_layout()
    plt.grid(True)

    # 标注峰值
    max_memory_index = memory_usages.index(max(memory_usages))
    plt.annotate(f"{memory_usages[max_memory_index]:.2f}%", 
                 (timestamps[max_memory_index], memory_usages[max_memory_index]), 
                 textcoords="offset points", xytext=(0, 10), ha='center', fontproperties=font_prop)

    # 保存图像到 img 目录
    filename = f"server_memory_usage_{timestamps[0].strftime('%Y%m%d%H%M%S')}_{timestamps[-1].strftime('%Y%m%d%H%M%S')}.png"
    plt.savefig(os.path.join(img_dir, filename))
    plt.close()
    print(f"已生成并保存服务器内存使用情况折线图：{filename}")

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
        timestamps, memory_usages = parse_log_data(start_time, end_time)
        plot_memory_usage(timestamps, memory_usages, f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
