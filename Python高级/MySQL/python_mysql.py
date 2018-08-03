# 创建connection象
# 创建cursor对象
# 编写sql语句
# 执行语句
# 更新操作需要commit方法提交
# 关闭cursor对象
# 关闭connection对象
from pymysql import *


def update():
    # 创建connection对象
    conn = connect(host="localhost", port=3306, database="jing_dong", user="root", password="mysql", charset="utf8")
    # 创建cursor对象
    cur = conn.cursor()
    # 编写sql语句
    sql = "insert into goods_cates(name) values ('ps4')"
    # 执行sql语句，并返回受影响的行数
    count = cur.execute(sql)
    print(count)
    # 提交
    conn.commit()
    # 关闭cursor对象
    cur.close()
    # 关闭connection对象
    conn.close()


def select():
    # 创建connection对象
    conn = connect(host="localhost", port=3306, database="jing_dong", user="root", password="mysql", charset="utf8")
    # 创建cursor对象
    cur = conn.cursor()
    # 编写sql语句
    sql = "select distinct name from goods_cates"
    # 执行sql语句，并返回受影响的行数
    count = cur.execute(sql)
    print(count)
    # fetchone 逐条返回内容
    for _ in range(count):
        ret = cur.fetchone()
        print(ret)
    # fetchall 一次返回全部内容
    """cursor对象又叫游标对象，当fetchone执行完后，指针已经移到最后所以，再fetchall返回的是一个空元组"""
    ret = cur.fetchall()
    print(ret)
    # connection 属性获取当前连接对象
    print(cur.connection)
    # 关闭cursor对象
    cur.close()
    # 关闭connection对象
    conn.close()


def main():
    update()
    select()

if __name__ == '__main__':
    main()