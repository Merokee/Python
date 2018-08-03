import multiprocessing
import time

def restaurantOne():
    while True:
        print("进程1正在操作！")
        time.sleep(1)

def restaurantTwo():
    while True:
        print("进程2正在操作！")
        time.sleep(1)

p1 = multiprocessing.Process(target=restaurantOne)
p2 = multiprocessing.Process(target=restaurantTwo)

p1.start()
p2.start()
