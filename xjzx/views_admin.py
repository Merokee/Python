from flask import Blueprint, render_template, request, redirect, session, g, current_app
from models import db, NewsInfo, UserInfo
from datetime import datetime

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


# 登陆处理
@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        dict1 = request.form
        mobile = dict1.get('mobile')
        pwd = dict1.get('pwd')
        if not all([mobile, pwd]):
            msg = '账号密码不能为空！'
            return render_template('admin/login.html', msg=msg)
        admin_user = UserInfo.query.filter_by(mobile=int(mobile), isAdmin=True).first()
        if admin_user is None:
            msg = '账号不存在！'
            return render_template('admin/login.html', msg=msg)
        else:
            if (admin_user.check_pwd(pwd)):
                session['admin_id'] = admin_user.id
                return redirect('/admin/')
            else:
                msg = '密码错误！'
                return render_template('admin/login.html', msg=msg)


# 登陆验证
@admin_blueprint.before_request
def index():
    if request.path != '/admin/login':
        if 'admin_id' not in session:
            return redirect('/admin/login')
        g.user = UserInfo.query.get(session['admin_id'])


# 后台首页
@admin_blueprint.route('/')
def index():
    return render_template('admin/index.html', user=g.user)


# 退出
@admin_blueprint.route('/logout')
def logout():
    del session['admin_id']
    return redirect('/admin/login')


# 用户统计
@admin_blueprint.route('/user_count')
def user_count():
    now = datetime.now()
    all_count = UserInfo.query.filter_by(isAdmin=False).count()
    month_count = UserInfo.query.filter(UserInfo.create_time >= datetime(now.year, now.month, 1)).count()
    day_count = UserInfo.query.filter(UserInfo.create_time >= datetime(now.year, now.month, now.day)).count()
    key = 'login%d_%d_%d' % (now.year, now.month, now.day)
    hour_list = current_app.redis.hkeys(key)
    hour_list = [hour.decode() for hour in hour_list]
    count_list = []
    for hour in hour_list:
        count_list.append(int(current_app.redis.hget(key, hour)))
    return render_template('admin/user_count.html',
                           all_count=all_count,
                           month_count=month_count,
                           day_count=day_count,
                           hour_list=hour_list,
                           count_list=count_list)


# 用户列表
@admin_blueprint.route('/user_list')
def user_list():
    page = int(request.args.get('page', '1'))
    pagination = UserInfo.query.filter_by(isAdmin=False).order_by(UserInfo.create_time).paginate(page, 10, False)
    user_list = pagination.items
    total_page = pagination.pages
    return render_template('admin/user_list.html',
                           user_list=user_list,
                           total_page=total_page,
                           page=page)


# 新闻审核
@admin_blueprint.route('/news_review')
def news_review():
    return render_template('admin/news_review.html')


# 新闻版式编辑
@admin_blueprint.route('/news_edit')
def news_edit():
    return render_template('admin/news_edit.html')


# 新闻分类管理
@admin_blueprint.route('/news_type')
def news_type():
    return render_template('admin/news_type.html')
