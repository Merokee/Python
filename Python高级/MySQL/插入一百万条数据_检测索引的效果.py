from pymysql import *


def update():
    # 创建connection对象
    conn = connect(host="localhost", port=3306, database="jing_dong", user="root", password="mysql", charset="utf8")
    # 创建cursor对象
    cur = conn.cursor()
    for i in range(1000000):
        # 编写sql语句
        sql = "insert into demo(name) values ('hah-%d')" % i
        # 执行sql语句，并返回受影响的行数
        count = cur.execute(sql)
    print(count)
    # 提交
    conn.commit()
    # 关闭cursor对象
    cur.close()
    # 关闭connection对象
    conn.close()


def main():
    update()


if __name__ == '__main__':
    main()