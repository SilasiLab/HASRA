import psutil
from time import sleep

def work_in_free_time(window_length=5, interval=3, threshold=0.3):
    cpu_pct = 0
    for i in range(window_length):
        cpu_pct += psutil.cpu_percent()
        sleep(interval)
    cpu_pct_ave = cpu_pct/float(window_length)
    print("cpu usage :%.4f" % cpu_pct_ave)
    if cpu_pct_ave < threshold:
        return True
    return False

if __name__ == '__main__':
    while(True):
        work_in_free_time(1, 2)