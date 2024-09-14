# 监控服务器进程内存使用，绘制折线图
排查问题自用小监控
### 1、安装依赖
```bash
pip install -r requirements.txt
```
### 2、记录
monitor.py记录每秒进程的内存使用情况取前20输出到monitor.log保存
```bash
nohup python monitor_process.py > monitor.log 2>&1 &
```
monitor.py记录每秒服务器的内存使用情况取前20输出到server_memory.log保存
nohup python monitor_server.py > server_memory.log 2>&1 &

### 3、绘制进程内存使用情况折线图
```bash
sudo python plot_memory_usage.py
1: 最近30秒
2: 最近1分钟
3: 最近5分钟
4: 最近30分钟
5: 最近1小时
6: 最近3小时
7: 最近6小时
8: 最近12小时
9: 最近24小时
10: 用户自选时间段
请输入选项编号: 10
请输入时间范围 (格式: YYYYMMDDHHMMSS-YYYYMMDDHHMMSS):
```
### 3、绘制服务器内存使用情况折线图
```bash
sodu python plot_server_memory.py
1: 最近30秒
2: 最近1分钟
3: 最近5分钟
4: 最近30分钟
5: 最近1小时
6: 最近3小时
7: 最近6小时
8: 最近12小时
9: 最近24小时
10: 用户自选时间段
请输入选项编号: 10
请输入时间范围 (格式: YYYYMMDDHHMMSS-YYYYMMDDHHMMSS):
```
![memory_usage_python_521346_20240914155646_20240914160146](https://github.com/user-attachments/assets/4c35daa5-fc06-49cc-a707-03430e6b9801)


### 错误排查
findfont: Generic family ‘sans-serif’ not found because none of the following families were found: SimHei  
https://topk-li.github.io/2024/09/14/matplotlib-zi-ti-wen-ti/
