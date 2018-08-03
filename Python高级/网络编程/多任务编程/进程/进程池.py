import os, time, random, multiprocessing


def worker(i):
    startTime = time.time()
    print(i, "开始执行，进程号为：%d" % os.getpid())
    time.sleep(random.random()*2)
    endTime = time.time()
    print(i, "执行完毕，耗时%0.2f:" % (endTime - startTime))


def main():
    po = multiprocessing.Pool(3)
    # 利用进程池执行目标函数20次
    for i in range(20):
        po.apply_async(worker, (i, ))

    print("---start---")
    po.close()
    po.join()
    print("---end---")


if __name__ == "__main__":
    main()
