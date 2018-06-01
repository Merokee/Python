from flask import Blueprint, jsonify, request
from flask import render_template, session
from models import db, UserInfo, NewsCategory, NewsInfo

news_blueprint = Blueprint('news', __name__)


# 首页
@news_blueprint.route('/')
def index():
    user = None
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = UserInfo.query.get(user_id)
    category_list = NewsCategory.query.all()
    news_rank = NewsInfo.query.order_by(NewsInfo.click_count.desc())[0:6]
    return render_template('news/index.html', title='首页-新经资讯', user=user, category_list=category_list, news_rank=news_rank)


# 新闻列表
@news_blueprint.route('/newslist')
def newslist():
    category_id = int(request.args.get('category_id'))
    page = int(request.args.get('page'))
    pagination = NewsInfo.query
    if not category_id:
        pagination=pagination.order_by(NewsInfo.update_time.desc()).paginate(page, 4, False)
    else:
        pagination=pagination.filter_by(category_id=category_id).order_by(NewsInfo.update_time.desc()).paginate(page, 4, False)
    news_list = pagination.items
    news_list1 = []
    for news in news_list:
        dict1 = {'id': news.id, 'pic_url':news.pic_url, 'title':news.title, 'content':news.content, 'user_avatar_url':news.user.avatar_url, 'user_id':news.user_id, 'user_nick_name':news.user.nick_name, 'update_time':news.update_time}
        news_list1.append(dict1)
    return jsonify(news_list=news_list1, page=page)
