def calcTime(*args):
    totalMinute = 0
    totalSeconds = 0
    for num in args:
        minute = int(num)
        totalMinute += minute
        seconds = num - minute
        totalSeconds += seconds
    totalSeconds += totalMinute * 60
    rate = 1.8
    totalSeconds /= rate
    # 先求小时
    hour = totalSeconds // 3600
    # 求分钟
    totalSeconds %= 3600
    minute = totalSeconds // 60
    return "共花时间%d小时%d分钟" %(hour, minute)

if __name__ == '__main__':
    # print(calcTime(12.04,12.32,13.40,13.16,12.56,9.02,15.22))
    from pathlib import Path

    path = r"C:\Users\17634\Desktop"
    p = Path(path)
    for p2 in p.iterdir():
        if '唐宇迪课程资料' in str(p2):
            print(list(p2.iterdir()))