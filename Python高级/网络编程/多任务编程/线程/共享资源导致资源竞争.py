import threading
import time

gnum = 1

def one(n):
    for _ in range(n):
        global gnum
        mutex.acquire()  # 上锁
        gnum += 1
        mutex.release()  # 解锁
    print(gnum)
        
def two(n):
    for _ in range(n):
        global gnum
        mutex.acquire()  # 上锁
        gnum += 1
        mutex.release()  # 解锁
    print(gnum)

# 创建互斥锁
mutex = threading.Lock()
t1 = threading.Thread(target=one, args=(10000000, ))
t2 = threading.Thread(target=two, args=(10000000, ))

t1.start()
t2.start()

time.sleep(3)

print(gnum)
