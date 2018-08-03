import greenlet
import time


def test1():
    while True:
        print("---test1---")
        gr2.switch()
        time.sleep(0.5)


def test2():
    while True:
        print("---test2---")
        gr1.switch()
        time.sleep(0.5)
   

# 创建两个协程，用obj.switch()来转换协程
gr1 = greenlet.greenlet(test1)
gr2 = greenlet.greenlet(test2)

gr1.switch()
