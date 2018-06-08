import random
from models import db, UserInfo, NewsInfo, NewsCategory
import re
from utils.ytx_sdk import ytx_send
from flask import Blueprint, session, jsonify, current_app, render_template, redirect
from flask import make_response, abort
from flask import request
import functools
from utils.upload_pic import upload_pic
from utils.captcha.captcha import captcha
from datetime import datetime

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
    if image_yzm.upper() != session['image_yzm']:
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
    mobile = dict1['mobile']
    pwd = dict1['pwd']
    # 验证
    if not all([mobile, pwd]):
        return jsonify(result=1)  # 请输入账号密码
    user = UserInfo.query.filter_by(mobile=mobile).first()
    if not user:
        return jsonify(result=2)  # 用户不存在
    else:
        if user.check_pwd(pwd):
            session['user_id'] = user.id
            # 修改登陆时间
            user.update_time = datetime.now()
            # 取出redis中的值加1再保存
            now = datetime.now()
            hour_list = ["08:15", "09:15", "10:15", "11:15", "12:15", "13:15", "14:15", "15:15", "16:15", "17:15",
                         "18:15", "19:15"]
            key = 'login%d_%d_%d' % (now.year, now.month, now.day)
            for index, item in enumerate(hour_list):

                if now.hour <= index + 8 or (now.hour == index + 8 and now.minute <= 15):
                    count = current_app.redis.hget(key, item)
                    if count:
                        count = int(count)
                    else:
                        count = 0  # 防止redis中无数据int方法报错
                    count += 1
                    current_app.redis.hset(key, item, count)
                    break
            else:
                count = int(current_app.redis.hget(key, "19:15"))
                count += 1
                current_app.redis.hset(key, "19:15", count)
            return jsonify(result=3, avatar=user.avatar_url, nick_name=user.nick_name)
        else:
            return jsonify(result=4)  # 密码错误


# 退出
@user_blueprint.route('/logout', methods=['POST'])
def logout():
    del session['user_id']
    return jsonify(result=1)


# # 显示登入图标
# @user_blueprint.route('/show')
# def show():
#     if 'user_id' in session:
#         return jsonify(result=1)
#     else:
#         return jsonify(result=2)


# 定义一个登陆验证装饰器
def login_requires(f1):
    @functools.wraps(f1)
    def func1(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/')
        return f1(*args, **kwargs)

    return func1


# 显示用户中心
@user_blueprint.route('/')
@login_requires
def user():
    user_id = session.get('user_id')
    user = UserInfo.query.get(user_id)
    return render_template('news/user.html', user=user, title='用户中心')


# 基本资料
@user_blueprint.route('/base', methods=['GET', 'POST'])
@login_requires
def base():
    user_id = session.get('user_id')
    user = UserInfo.query.get(user_id)
    if request.method == 'GET':
        return render_template('news/user_base_info.html', user=user)
    elif request.method == 'POST':
        dict1 = request.form
        signature = dict1.get('signature')
        nick_name = dict1.get('nick_name')
        gender = dict1.get('gender')
        # 修改数据库的值
        user.signature = signature
        user.nick_name = nick_name
        user.gender = True if gender == 'True' else False
        try:
            db.session.commit()
        except:
            current_app.logger_xjzx.error('修改签名时，访问数据库失败')
            return
        return jsonify(result=1)


# 头像设置
@user_blueprint.route('/pic', methods=['GET', 'POST'])
@login_requires
def pic():
    user_id = session.get('user_id')
    user = UserInfo.query.get(user_id)
    if request.method == 'GET':
        return render_template('news/user_pic_info.html', user=user)
    elif request.method == 'POST':
        f1 = request.files.get('avatar')
        avatar = upload_pic(f1)
        user.avatar = avatar
        try:
            db.session.commit()
        except:
            current_app.logger_xjzx.error('上传头像时，访问数据库失败')
            return jsonify(result=0)
        return jsonify(result=1, avatar_url=user.avatar_url)


# 我的关注
@user_blueprint.route('/follow')
@login_requires
def follow():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    # 获取当前页码
    page = int(request.args.get('page', '1'))
    # 分页显示
    pagination = user.follow_user.paginate(page, 4, False)
    user_list = pagination.items
    total_page = pagination.pages

    return render_template(
        'news/user_follow.html',
        user_list=user_list,
        total_page=total_page,
        page=page)


# 密码修改
@user_blueprint.route('/pwd', methods=['GET', 'POST'])
@login_requires
def pwd():
    # 展示页面
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')

    # 修改密码
    elif request.method == 'POST':
        user_id = session['user_id']
        user = UserInfo.query.get(user_id)
        # 获取当前密码，新密码和确认密码
        dict1 = request.form
        pwd = dict1.get('pwd', '')
        new_pwd = dict1.get('new_pwd', '')
        sure_pwd = dict1.get('sure_pwd', '')

        # 逻辑判断
        if not re.match(r'[a-zA-Z0-9_]{6,20}', pwd):
            return render_template('news/user_pass_info.html', msg='密码错误！')

        if not all([pwd, new_pwd, sure_pwd]):
            return render_template('news/user_pass_info.html', msg='密码不能为空！')

        if new_pwd != sure_pwd:
            return render_template('news/user_pass_info.html', msg='确认密码输入错误！')

        user.password = pwd
        try:
            db.session.commit()
        except:
            current_app.logger_xjzx.error('修改密码时，访问数据库失败')
            return render_template('news/user_pass_info.html', msg='服务器睡着了，修改密码失败！')
        return render_template('news/user_pass_info.html', msg='修改密码成功！')


# 我的收藏
@user_blueprint.route('/collection')
@login_requires
def collection():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    page = int(request.args.get('page', '1'))
    pagination = user.news_collect.order_by(NewsInfo.update_time.desc()).paginate(page, 6, False)
    total_page = pagination.pages
    collect_list = pagination.items
    return render_template(
        'news/user_collection.html',
        collect_list=collect_list,
        total_page=total_page,
        page=page)


# 新闻发布
@user_blueprint.route('/release', methods=['GET', 'POST'])
@login_requires
def release():
    news = None
    news_id = request.args.get('news_id')
    category_list = NewsCategory.query.all()
    # 展示页面
    if request.method == 'GET':
        # 展示发布（无内容）
        if news_id is None:
            return render_template(
                'news/user_news_release.html',
                news=news,
                category_list=category_list)
        # 从新闻列表跳转过来，展示编辑（有内容）
        else:
            news = NewsInfo.query.get(news_id)
            return render_template(
                'news/user_news_release.html',
                news=news,
                category_list=category_list)
    # 表单提交
    elif request.method == 'POST':
        dict1 = request.form
        title = dict1.get('title')
        category = int(dict1.get('category'))
        summary = dict1.get('summary')
        pic = request.files.get('pic')
        content = dict1.get('content')
        # 编辑 不一定跟换图片
        if news_id:
            if not all([title, category, summary, content]):
                return render_template(
                    'news/user_news_release.html',
                    news=news, msg='请完善新闻信息',
                    category_list=category_list)
            news = NewsInfo.query.get(news_id)
        # 发布 需要提交图片 并新建对象
        else:
            if not all([title, category, summary, pic, content]):
                return render_template('news/user_news_release.html',
                                       news=news, msg='请完善新闻信息',
                                       category_list=category_list)
            news = NewsInfo()
        # 有图片上传到七牛云
        if pic:
            news.pic = upload_pic(pic)
        # 给属性赋值，注意update_time,user_id字段必需赋值
        news.title = title
        news.summary = summary
        news.content = content
        news.status = 1
        news.update_time = datetime.now()
        news.category_id = category
        news.user_id = session['user_id']
        # 保存成功转到新闻列表
        try:
            db.session.add(news)
            db.session.commit()
        except:
            current_app.logger_xjzx.error('修改新闻内容时，访问数据库失败')
            return render_template('news/user_pass_info.html', msg='服务器睡着了，修改新闻内容失败！')
        else:
            return redirect('/user/newslist')


# 新闻列表
@user_blueprint.route('/newslist')
@login_requires
def newslists():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    page = int(request.args.get('page', '1'))
    pagination = user.news.order_by(NewsInfo.update_time.desc()).paginate(page, 6, False)
    total_page = pagination.pages
    news_list = pagination.items
    return render_template('news/user_news_list.html',
                           page=page, news_list=news_list,
                           total_page=total_page)


# 作者页
@user_blueprint.route('/<int:author_id>')
def other(author_id):
    user = None
    author = UserInfo.query.get(author_id)
    if author is None:
        abort(404)
    if 'user_id' in session:
        user = UserInfo.query.get(session['user_id'])
    page = int(request.args.get('page', '1'))
    pagination = author.news.order_by(NewsInfo.update_time.desc()).paginate(page, 6, False)
    total_page = pagination.pages
    news_list = pagination.items
    return render_template('news/other.html',
                           title='用户概况',
                           user=user,
                           author=author,
                           page=page,
                           news_list=news_list,
                           total_page=total_page)
