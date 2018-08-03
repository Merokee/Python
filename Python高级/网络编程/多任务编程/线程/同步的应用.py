"""
同步：协同步调,按预定的先后次序进行运行
异步: 运行的次序不确定
"""
# 创建一个同步多线程

import threading
import time


class work1(threading.Thread):
    def run(self):
        while True:
            if lock1.acquire():
                print("---work1----")
                time.sleep(0.5)
                lock2.release()
        

class work2(threading.Thread):
    def run(self):
        while True:
            if lock2.acquire():
                print("---work2----")
                time.sleep(0.5)
                lock3.release()


class work3(threading.Thread):
    def run(self):
        while True:
            if lock3.acquire():
                print("---work3----")
                time.sleep(0.5)
                lock1.release()
                

lock1 = threading.Lock()
lock2 = threading.Lock()
lock2.acquire()
lock3 = threading.Lock()
lock3.acquire()
w1 = work1()
w2 = work2()
w3 = work3()
w1.start()
w2.start()
w3.start()


