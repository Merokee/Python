import multiprocessing
import time

gum = 666

def restaurantOne():
    gum = 555
    print("进程1正在操作！", gum)
    time.sleep(1)

def restaurantTwo():
    print("进程2正在操作！", gum)
    time.sleep(1)

p1 = multiprocessing.Process(target=restaurantOne)
p2 = multiprocessing.Process(target=restaurantTwo)

p1.start()
p1.join()
p2.start()
p2.join()
print(gum)
