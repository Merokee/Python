from flask import Blueprint, jsonify, request, current_app
from flask import render_template, session, abort
from models import db, UserInfo, NewsCategory, NewsInfo, NewsComment, tb_news_collect

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
    return render_template('news/index.html', title='首页-新经资讯', user=user, category_list=category_list,
                           news_rank=news_rank)


# 新闻列表
@news_blueprint.route('/newslist')
def newslist():
    category_id = int(request.args.get('category_id'))
    page = int(request.args.get('page'))
    pagination = NewsInfo.query
    if not category_id:
        pagination = pagination.order_by(NewsInfo.update_time.desc()).paginate(page, 4, False)
    else:
        pagination = pagination.filter_by(category_id=category_id).order_by(NewsInfo.update_time.desc()).paginate(page,
                                                                                                                  4,
                                                                                                                  False)
    news_list = pagination.items
    news_list1 = []
    for news in news_list:
        dict1 = {'id': news.id, 'pic_url': news.pic_url, 'title': news.title, 'summary': news.summary,
                 'user_avatar_url': news.user.avatar_url, 'user_id': news.user_id,
                 'user_nick_name': news.user.nick_name, 'update_time': news.update_time.strftime('%Y-%m-%d %H:%M:%S')}
        news_list1.append(dict1)
    return jsonify(news_list=news_list1, page=page)


# 文章详情页
@news_blueprint.route('/<int:news_id>')
def detail(news_id):
    user = None
    if 'user_id' in session:
        user = UserInfo.query.get(int(session['user_id']))
    # [0:6]在查询是添加查询条数限定limit(6),并不是查询所有然后取前6个，不等同与列表切片操作！
    news_rank = NewsInfo.query.order_by(NewsInfo.click_count.desc())[0:6]
    news = NewsInfo.query.get(news_id)
    if news is None:
        abort(404)
    else:
        # 刷新点击量
        news.click_count += 1
        db.session.commit()
        return render_template('news/detail.html',
                               title='文章详情页',
                               user=user,
                               news_rank=news_rank,
                               news=news)


# 收藏
@news_blueprint.route('/collection/<int:news_id>', methods=['POST'])
def collection(news_id):
    action = request.form.get('action')  # 标记是收藏请求还是取消收藏
    news = NewsInfo.query.get(news_id)
    if news is None:
        # abort(404)
        return jsonify(result=1)  # 拒绝无效访问
    if 'user_id' not in session:
        return jsonify(result=2)  # 防止未登录刷收藏
    user = UserInfo.query.get(int(session['user_id']))
    if action is not None:
        if news not in user.news_collect:
            return jsonify(result=5)  # 未收藏就不用取消收藏了
        user.news_collect.remove(news)
    else:
        if news in user.news_collect:
            return jsonify(result=3)  # 判断是否已经收藏
        user.news_collect.append(news)

    try:
        db.session.commit()
    except:
        current_app.logger_xjzx.error('收藏新闻时，访问数据库失败')
        return jsonify(result=6)
    else:
        return jsonify(result=4)


# 发表评论
@news_blueprint.route('/comment/add', methods=['POST'])
def comment():
    if 'user_id' not in session:
        return jsonify(result=2)  # 防止未登录刷评论
    user_id = session.get('user_id')
    dict1 = request.form
    news_id = int(dict1.get('news_id'))
    msg = dict1.get('msg')
    if not all([msg, news_id]):
        return jsonify(result=3)  # 没有评论内容
    news = NewsInfo.query.get(news_id)
    if news is None:
        # abort(404)
        return jsonify(result=1)  # 拒绝无效访问

    # 新建评论
    comment = NewsComment()
    comment.msg = msg
    comment.news_id = news_id
    comment.user_id = user_id
    db.session.add(comment)

    # 评论数加1
    news.comment_count += 1

    # 提交
    try:
        db.session.commit()
    except:
        current_app.logger_xjzx.error('收藏新闻时，访问数据库失败')
        return jsonify(result=5)
    else:
        return jsonify(result=4,
                       comment_count=news.comment_count)


# 显示评论
@news_blueprint.route('/comment/show')
def show_comments():
    user_id = session.get('user_id')
    news_id = request.args.get('news_id')
    comment_list = NewsComment.query.filter_by(news_id=news_id,comment_id=None).order_by(NewsComment.update_time.desc())
    comment_list1 = []
    up_list = current_app.redis.lrange('commentup%d'%user_id, 0, -1)
    up_list = [int(cid) for cid in up_list]
    for comment in comment_list:
        if comment.id in up_list:
            is_like = 1
        else:
            is_like = 0
        reply_list = comment.comments
        reply_list1=[]
        for reply in reply_list:
            dict2 = {
                'nick_name':reply.user.nick_name,
                'msg':reply.msg
            }
            reply_list1.append(dict2)
        dict1 = {'user_avatar_url': comment.user.avatar_url,
                 'user_nick_name': comment.user.nick_name,
                 'comment': comment.msg,
                 'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                 'id': comment.id,
                 'like_count': comment.like_count,
                 'is_like':is_like,
                 'reply_list':reply_list1
                 }
        comment_list1.append(dict1)
    return jsonify(result=2,
                   comment_list=comment_list1)


# 关注取消关注
@news_blueprint.route('/userfollow', methods=['POST'])
def userfollow():
    dict1 = request.form
    follow_user_id = dict1.get('follow_user_id')
    action = int(dict1.get('action'))
    if 'user_id' not in session:
        return jsonify(result=1)
    origin_user = UserInfo.query.get(int(session['user_id']))
    follow_user = UserInfo.query.get(int(follow_user_id))
    if action == 1:
        follow_user.follow_count += 1
        origin_user.follow_user.append(follow_user)
    else:
        follow_user.follow_count -= 1
        origin_user.follow_user.remove(follow_user)
    db.session.commit()
    return jsonify(result=2, follow_count=follow_user.follow_count)


# 点赞/取消点赞
@news_blueprint.route('/commentup', methods=['POST'])
def commentup():
    if 'user_id' not in session:
        return jsonify(result=1)
    user_id = session['user_id']
    dict1 = request.form
    action = int(dict1['action'])
    comment_id = int(dict1['comment_id'])
    comment = NewsComment.query.get(comment_id)

    if action == 1:
        # 点赞
        current_app.redis.lpush('commentup%d' % user_id, comment_id)
        comment.like_count += 1
    else:
        # lrem key count value
        current_app.redis.lrem('commentup%d' % user_id, 0, comment_id)
        # 取消点赞
        comment.like_count -= 1
    db.session.commit()
    return jsonify(result=2, like_count=comment.like_count)


# 回复评论
@news_blueprint.route('/replycomment', methods=['POST'])
def replycomment():
    if 'user_id' not in session:
        return jsonify(result=1)
    user_id = session['user_id']
    dict1 = request.form
    comment_id = int(dict1['comment_id'])
    msg = dict1['msg']
    news_id = int(dict1['news_id'])
    if not all([comment_id, msg, news_id]):
        return jsonify(result=2)
    comment = NewsComment()
    comment.comment_id=comment_id
    comment.msg = msg
    comment.user_id = user_id
    comment.news_id = news_id
    db.session.add(comment)
    db.session.commit()
    return jsonify(result=3)