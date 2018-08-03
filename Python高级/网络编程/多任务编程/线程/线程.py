import time
import threading

def tableOne():
    for i in range(5):
        print("为操作111111111服务") 
        time.sleep(1)

def tableTwo():
    for i in range(5):
        print("为餐桌2222222服务")
        time.sleep(1)

print(threading.enumerate())
t2 = threading.Thread(target=tableTwo)
t2.start()
print(threading.enumerate())
t1 = threading.Thread(target=tableOne)
t1.start()

print(threading.enumerate())

for i in range(5):
    print("主线程正在工作！")
    time.sleep(1)

