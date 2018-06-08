from flask import Blueprint, render_template, request, redirect, session, g, current_app, jsonify
from models import db, NewsInfo, UserInfo, NewsCategory
from datetime import datetime
from utils.upload_pic import upload_pic

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


# 返回新闻列表json数据
@admin_blueprint.route('/news_review_json')
def news_review_json():
    page = int(request.args.get('page', '1'))
    input_txt = request.args.get('input_txt')
    pagination = NewsInfo.query
    if input_txt is None:
        pagination = pagination.order_by(NewsInfo.create_time).paginate(page, 10, False)
    else:
        pagination = pagination.filter(NewsInfo.title.contains(input_txt)).paginate(page, 10, False)
    total_page = pagination.pages
    news_list = pagination.items
    news_list1 = []
    for news in news_list:
        dict1 = {'id': news.id,
                 'title': news.title,
                 'update_time': news.update_time.strftime('%Y-%m-%d %H-%M-%S'),
                 'status': news.status}
        news_list1.append(dict1)
    return jsonify(news_list=news_list1,
                   total_page=total_page)


# 显示审核页面
@admin_blueprint.route('/news_review_detail/<int:news_id>', methods=['GET', 'POST'])
def news_review_detail(news_id):
    news = NewsInfo.query.get(news_id)
    if request.method == 'GET':
        return render_template('admin/news_review_detail.html', news=news)
    elif request.method == 'POST':
        action = request.form.get('action')
        reason = request.form.get('reason')
        if action == 'accept':
            news.status = 2
        else:
            news.status = 3
            news.reason = reason
        db.session.commit()
        return redirect('/admin/news_review')


# 新闻版式编辑
@admin_blueprint.route('/news_edit')
def news_edit():
    return render_template('admin/news_edit.html')


# 返回新闻列表json数据
@admin_blueprint.route('/news_edit_json')
def news_edit_json():
    page = int(request.args.get('page', '1'))
    input_txt = request.args.get('input_txt')
    pagination = NewsInfo.query
    if input_txt is None:
        pagination = pagination.order_by(NewsInfo.update_time).paginate(page, 10, False)
    else:
        pagination = pagination.filter(NewsInfo.title.contains(input_txt)).paginate(page, 10, False)
    news_list = pagination.items
    total_page = pagination.pages
    news_list1 = []
    for news in news_list:
        dict1 = {
            'id': news.id,
            'title': news.title,
            'update_time': news.update_time.strftime('%Y-%m-%d %H-%M-%S')
        }
        news_list1.append(dict1)
    return jsonify(total_page=total_page, news_list=news_list1)


# 显示编辑界面
@admin_blueprint.route('/news_edit_detail/<int:news_id>', methods=['GET', 'POST'])
def news_edit_detail(news_id):
    news = NewsInfo.query.get(news_id)
    if request.method == 'GET':
        category_list = NewsCategory.query.all()
        return render_template(
            'admin/news_edit_detail.html',
            news=news,
            category_list=category_list
        )
    elif request.method == 'POST':
        dict1 = request.form
        title = dict1.get('title')
        category_id = dict1.get('category_id')
        summary = dict1.get('summary')
        content = dict1.get('content')
        # 接收图片文件
        pic = request.files.get('pic')
        if pic:
            pic_name = upload_pic(pic)
            news.pic = pic_name
        # 修改对象的属性
        news.title = title
        news.category_id = int(category_id)
        news.summary = summary
        news.content = content
        news.update_time = datetime.now()
        # 保存
        db.session.commit()
        # 响应
        return redirect('/admin/news_edit')


# 新闻分类管理
@admin_blueprint.route('/news_type')
def news_type():
    return render_template('admin/news_type.html')


# 返回分类列表json数据
@admin_blueprint.route('/news_type_json')
def news_type_json():
    category_list = NewsCategory.query.all()
    list1 = []
    for category in category_list:
        dict1 = {
            'id': category.id,
            'name': category.name
        }
        list1.append(dict1)
    return jsonify(category_list=list1)


# 添加分类
@admin_blueprint.route('/add_category', methods=['POST'])
def add_category():
    name = request.form.get('name')
    if name is None:
        return jsonify(result=0)
    count = NewsCategory.query.filter_by(name=name).count()
    if count > 0:
        return jsonify(result=2)
    category = NewsCategory()
    category.name = name
    db.session.add(category)
    db.session.commit()
    return jsonify(result=1)


# 修改分类
@admin_blueprint.route('/change_category', methods=['POST'])
def change_category():
    dict1 = request.form
    id = dict1.get('id')
    name = dict1.get('name')
    print(id, name)
    if not all([id, name]):
        return jsonify(result=0)
    count = NewsCategory.query.filter_by(name=name).count()
    if count > 0:
        return jsonify(result=-1)
    # category = NewsCategory.query.filter_by(name=name)  # 返回的是sql语句,不能直接用if来判断
    # if category:
    #     print(category)
    category = NewsCategory.query.get(id)
    category.name = name
    db.session.commit()
    return jsonify(result=1)
