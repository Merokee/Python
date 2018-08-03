# 创建connection象
# 创建cursor对象
# 编写sql语句
# 执行语句
# 更新操作需要commit方法提交
# 关闭cursor对象
# 关闭connection对象
from pymysql import *


class PythonMysql(object):
    def __init__(self):
        # 创建connection对象
        self.conn = connect(host="localhost", port=3306, database="card_system", user="root", password="mysql", charset="utf8")
        # 创建cursor对象
        self.cur = self.conn.cursor()

    def exe(self, sql):
        # 执行sql语句，并返回受影响的行数
        count = self.cur.execute(sql)
        return count

    def __del__(self):
        # 关闭cursor对象
        self.cur.close()
        # 关闭connection对象
        self.conn.close()

sql = None
pm = PythonMysql()


def update():
    # 编写sql语句
    sql = "insert into goods_cates(name) values ('ps4')"
    # 执行sql语句，并返回受影响的行数
    count = pm.exe(sql)
    print(count)
    # 提交
    pm.conn.commit()


def select():
    # 编写sql语句
    sql = "select * from card_system.card_datas"
    # 执行sql语句，并返回受影响的行数
    count = pm.exe(sql)
    print(count)
    # fetchone 逐条返回内容
    for _ in range(count):
        ret = pm.cur.fetchone()
        print(ret)
    # fetchall 一次返回全部内容
    """cursor对象又叫游标对象，当fetchone执行完后，指针已经移到最后所以，再fetchall返回的是一个空元组"""
    ret = pm.cur.fetchall()
    print(ret)
    # connection 属性获取当前连接对象
    print(pm.cur.connection)


def main():
    # update()
    select()

if __name__ == '__main__':
    main()