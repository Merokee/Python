# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-17 下午8:16
import unittest


class Test(unittest.TestCase):
    """
    python自带的测试单元
    """
    def setUp(self):  # 每个测试任务执行前执行
        print("111")

    def tearDown(self):  # 每个测试任务执行后执行
        print("222")

    def test_run_a(self):
        print("aaa")

    def test_run_b(self):
        print("bbb")

    @classmethod
    def setUpClass(cls):  # 测试开始前执行，只执行一次
        print("start")

    @classmethod
    def tearDownClass(cls):  # 测试结束前执行, 只执行一次
        print("end")


if __name__ == '__main__':
    unittest.main()
