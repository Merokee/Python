import threading
import time


class MyThread(threading.Thread):
    def run(self):
        while True:
            print("===痛也给痛===")
            time.sleep(1)

t = MyThread()
t.start()

while True:
    print("===哈哈哈====")
    time.sleep(1)
