import multiprocessing, os, time, random


def write(q):
    list1 = [x for x in range(10)]
    for x in list1:
        print("%d写入程序操作起来了！" % os.getpid())
        q.put(x)
        time.sleep(random.random())
        print(x , "放入队列成功!")


def read(q):
    for _ in range(10):
        print("%d阅读程序操作起来了！" % os.getpid())
        startTime = time.time()
        s = q.get()
        endTime = time.time()
        print("%s 被取出了！用了%.2f秒" % (s, endTime-startTime))


def main():
    print("%s进程开始" % os.getpid())
    # 创建一个进程池
    po = multiprocessing.Pool(2)
    # 生成一个队列
    q = multiprocessing.Manager().Queue()

    po.apply_async(write, (q, ))
    po.apply_async(read, (q, ))

    po.close()
    po.join()
    print("进程间传递参数完成!")
    
    
if __name__ == "__main__":
    main()
