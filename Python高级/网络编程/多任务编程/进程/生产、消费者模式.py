import multiprocessing
import time
import random


def write(q):
    """间断放入元素，模拟生产过程"""
    list1 = ["miss", "yular", "me"]
    for s in list1:
        q.put(s)
        time.sleep(random.random())
        print("%s已经写入" % s)


def read(q):
    for _ in range(3):
        startTime = time.time()
        s = q.get()
        endTime = time.time()
        print("%s已经读取成功，用时：%0.2f" % (s, endTime-startTime))
    

def main():
    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=write, args=(q, ))
    p2 = multiprocessing.Process(target=read, args=(q, ))

    p1.start()
    p2.start()



if __name__ == "__main__":
    main()
