from flask_script.commands import Command
from models import db, UserInfo
from datetime import datetime
import random
from flask import current_app


# 管理员注册
class CreateAdminUser(Command):
    def run(self):
        mobile = input('请输入账号：')
        pwd = input('请输入密码：')
        nick_name = input('nick_name:')
        admin_user = UserInfo()
        admin_user.nick_name = nick_name
        admin_user.mobile = mobile
        admin_user.password = pwd
        admin_user.isAdmin = True
        db.session.add(admin_user)
        db.session.commit()
        print('创建管理员账户成功！')


class RegisterUser(Command):
    def run(self):
        user_list = []
        for i in range(1, 1000):
            user = UserInfo()
            user.nick_name = '用户' + str(i)
            user.mobile = i
            user.isAdmin = False
            user.create_time = datetime(2018, random.randint(1, 6), random.randint(1, 28))
            user_list.append(user)
        db.session.add_all(user_list)
        db.session.commit()


# 用户登陆
class UserLogin(Command):
    def run(self):
        now = datetime.now()
        key = 'login%d_%d_%d' % (now.year, now.month, now.day)
        for i in range(8, 20):
            current_app.redis.hset(key, '%02d:15' % i, random.randint(100, 2000))
