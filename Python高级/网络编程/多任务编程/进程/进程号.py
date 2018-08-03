import multiprocessing
import time
import os

def restaurantOne():
    while True:
        print("进程号：%d,%d" % (os.getpid(), os.getppid()))
        print("进程1正在操作！")
        time.sleep(1)

def restaurantTwo():
    while True:
        print("进程号：%d,%d" % (os.getpid(), os.getppid()))
        print("进程2正在操作！")
        time.sleep(1)

def main():
    p1 = multiprocessing.Process(target=restaurantOne)
    p2 = multiprocessing.Process(target=restaurantTwo)

    p1.start()
    p2.start()
    while True:

        print("进程号：%d,%d" % (os.getpid(), os.getppid()))
        print("主进程正在操作！")
        time.sleep(1)

if __name__ == "__main__":
    main()
