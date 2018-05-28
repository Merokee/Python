import random
from models import db, UserInfo
import re
from utils.ytx_sdk import ytx_send
from flask import Blueprint, session, jsonify, current_app
from flask import make_response
from flask import request

from utils.captcha.captcha import captcha

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


# 图片验证>> 获取图片验证码　>>保存到session >> 指定解析类型  >> 修改js，动态改变src实现刷新验证码
@user_blueprint.route('/image_yzm')
def image_yzm():
    # 生成验证码
    name, text, buffer = captcha.generate_captcha()
    # 将text保存在session中
    session['image_yzm'] = text
    # 返回一个响应，指定返回解析类型是图片
    response = make_response(buffer)  # 返回的buffer是bytes
    response.mimetype = 'image/png'
    return response


# 短信验证>> 获取短信验证码 >> 保存到session　>> 返回到页面
@user_blueprint.route('/msm_yzm')
def msm_yzm():
    # 获取数据
    dict1 = request.args
    mobile = dict1['mobile']
    image_yzm = dict1['image_yzm']

    # 对比图片验证码
    if image_yzm.upper() != session['image_yzm']:
        return jsonify(result=1)
    # 判断手机号是否为空

    # 生成一个４位的随机数
    yzm = random.randint(1000, 9999)
    # 保存到ｓｅｓｓｉｏｎ
    session['msm_yzm'] = yzm
    # 发送短信验证

    # ytx_send.sendTemplateSMS(mobile, {yzm, 5}, 1)  # 发送短信验证码到手机
    # ytx_send.sendTemplateSMS(mobile, [yzm, '5'], 1)  # 发送短信
    print(yzm)
    return jsonify(result=2)


# 提交表单
@user_blueprint.route('/register', methods=['POST'])
def register():
    # 接受数据
    dict1 = request.form
    mobile = dict1['mobile']
    image_yzm = dict1['image_yzm']
    msm_yzm = dict1['msm_yzm']
    pwd = dict1['pwd']

    # 验证
    if not all([mobile, image_yzm, msm_yzm, pwd]):
        return jsonify(result=1)
    mobile_count = UserInfo.query.filter_by(mobile=mobile).count()  # 返回１或者０
    if mobile_count:
        return jsonify(result=2)  # 该号码已被注册
    if image_yzm != session['image_yzm']:
        return jsonify(result=3)  # 图片验证码错误
    if int(msm_yzm) != session['msm_yzm']:
        return jsonify(result=4)  # 短信验证码错误
    if not re.match(r'[a-zA-Z0-9_]{6,20}', pwd):
        return jsonify(result=5)  # 密码不符规范

    # 创建对象
    user = UserInfo()
    user.mobile = mobile
    user.nick_name = mobile
    user.password = pwd

    # 保存提交
    try:
        db.session.add(user)
        db.session.commit()
    except:
        current_app.logger_xjzx.error('注册用户时数据库访问失败')
        return jsonify(result=6)

    return jsonify(result=7)


# 登陆
@user_blueprint.route('/login', methods=['POST'])
def login():
    dict1 = request.form
    user_id = dict1['user_id']
    pwd = dict1['pwd']
    # 验证
    if not all([user_id, pwd]):
        return jsonify(result=1)  # 请输入账号密码
    user = UserInfo.query.filter_by(mobile=user_id).first()
    if not user:
        return jsonify(result=2)  # 用户不存在
    else:

        if user.check_pwd(pwd):
            session['user_id'] = user_id
            return jsonify(result=3, avatar=user.avatar, nick_name=user.nick_name)
        else:
            return jsonify(result=4)  # 密码错误


# 退出
@user_blueprint.route('/logout', methods=['POST'])
def logout():
    del session['user_id']
    return jsonify(result=1)


# 显示登入图标
@user_blueprint.route('/show')
def show():
    if 'user_id' in session:
        return jsonify(result=1)
    else:
        return jsonify(result=2)