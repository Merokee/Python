import gevent

def f(n):
    for i in range(n):
        print(gevent.getcurrent(), i)  # 获取协程号
        gevent.sleep(0.5)

g1 = gevent.spawn(f,5)  # 创建3个协程
g2 = gevent.spawn(f,5)
g3 = gevent.spawn(f,5)
g1.join()  # 让3个协程交替进行
g2.join()
g3.join()
