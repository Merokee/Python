from gevent import monkey
import gevent, random, time


# 有耗时操作时需要
monkey.patch_all()  # 将程序中用到耗时操作的代码，换为gevent中自己实现的模块


def coroutineWork(coroutineName):
    for i in range(10):
        print(coroutineName, i, gevent.getcurrent())
        time.sleep(random.random())


gevent.joinall([gevent.spawn(coroutineWork, "work1"), 
                gevent.spawn(coroutineWork, "work2"),
                gevent.spawn(coroutineWork, "work3")])

