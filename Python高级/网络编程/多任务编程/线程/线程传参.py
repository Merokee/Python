import threading
import time

# 定义一个全局变量

numList = [1, 2, 3]

def one(tmpList):
    tmpList.append(4)
    print(tmpList)

def two(tmpList):
    print(tmpList)

t1 = threading.Thread(target=one, args=(numList, ))
t2 = threading.Thread(target=two, args=(numList, ))

t1.start()
time.sleep(1)
t2.start()
time.sleep(1)

print(numList)

