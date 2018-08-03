# SQL注入, 不能使用拼接字符串的方式来写sql语句， 需要在execute方法中传参数

from pymysql import *


def select(idstr):
    # 创建connection对象
    conn = connect(host="localhost", port=3306, database="jing_dong", user="root", password="mysql", charset="utf8")
    # 创建cursor对象
    cur = conn.cursor()
    # 编写sql语句
    sql = "select distinct name from goods_cates where id = %s"
    # 执行sql语句，并返回受影响的行数
    count = cur.execute(sql, [idstr])
    print(count)
    # fetchall 一次返回全部内容
    ret = cur.fetchall()
    print(ret)
    # 关闭cursor对象
    cur.close()
    # 关闭connection对象
    conn.close()


def main():
    idstr = input("想查询的id：")
    select(idstr)

if __name__ == '__main__':
    main()