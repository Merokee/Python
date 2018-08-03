from pymysql import *
# 创建Python链接数据库的类
# 编写crud语句


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

pm = PythonMysql()


def update(sql):
    # 执行sql语句，并返回受影响的行数
    count = pm.exe(sql)
    print(count)
    # 提交
    pm.conn.commit()


def select(sql):
    count = pm.exe(sql)
    return count, pm.cur.fetchall()


list1 = ["id", "name", "Tel", "QQ", "E_mail"]


# 用户欢迎界面
def welcome():
    print("*_" * 15)
    print("欢迎使用【名片管理系统】 V1.0\n")
    print("1.新建名片")
    print("2.显示全部")
    print("3.查询名片")
    print("0.退出系统")
    print("")
    print("*_" * 15)


def new_card():
    name = input("请输入你的姓名：")
    Tel = input("请输入你的电话号码：")
    QQ = input("请输入QQ号码：")
    E_mail = input("请输入邮箱：")
    data = (name, Tel, QQ, E_mail)
    sql = "insert into card_datas (name, Tel, QQ, E_mail) values %s" % str(data)
    update(sql)


def print_table_head():
    print("_" * 30)
    for element in list1:
        print(element, end=" " * 5)
    print()


def show_all():
    print_table_head()
    sql = "select * from card_datas"
    count, ret = select(sql)
    if count == 0:
        print("无片可看！")
    else:
        print("系统名片数：", count)
        print(ret)


def print_card(info):
    print_table_head()
    for value in info.values():
        print(value, end=" " * 5)
    print()


def check_card():
    print("你选择的功能是：")
    print("3.查询名片\n")
    ck_name = input("请输入你想查询的名片姓名：")
    sql = "select * from card_datas where name = \'%s\'" % ck_name
    print(sql)
    count, ret = select(sql)
    if count == 0:
        print("无片可看！")
    else:
        print("系统名片数：", count)
        print(ret)
    del_change_card(ck_name)


def del_change_card(ck_name):
    while True:
        ctrl_name = input("请选择你想对该名片进行的操作：1.删除名片，2.修改名片，3.返回上一级")
        if ctrl_name == "1":
            sql = "delete from card_datas where name = \'%s\'" %ck_name
            update(sql)
            print("名片已删除！")
            break
        elif ctrl_name == "2":
            sql = "delete from card_datas where name = \'%s\'" % ck_name
            update(sql)
            new_card()
            print("名片修改成功！")
            break
        elif ctrl_name == "3":
            break
        else:
            print("你输入的操作错误，请重新输入！")
