from flask_sqlalchemy import SQLAlchemy, current_app
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

pymysql.install_as_MySQLdb()
from datetime import datetime


db = SQLAlchemy()


# 创建一个类定义共同字段
class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Boolean, default=False)


# 新闻分类
class NewsCategory(db.Model, BaseModel):
    __tablename__ = 'news_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    news = db.relationship('NewsInfo', backref='category', lazy='dynamic')  # 默认调用对象时执行操作，　使用lazy='dynamic',就改为调用属性是执行操作


# 新闻
class NewsInfo(db.Model, BaseModel):
    __tablename__ = 'news_info'
    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(50))
    title = db.Column(db.String(30))
    summary = db.Column(db.String(200))
    content = db.Column(db.Text)
    click_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    reason = db.Column(db.String(100), default='')
    category_id = db.Column(db.Integer, db.ForeignKey('news_category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    # 新闻１：ｎ新闻评论
    comments = db.relationship('NewsComment', backref='news', lazy='dynamic', order_by='NewsComment.id.desc()')


# 新闻m:n用户（收藏关系表）
tb_news_collect = db.Table(
    'tb_user_news',
    db.Column('user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True),
    db.Column('news_id', db.Integer, db.ForeignKey('news_info.id'), primary_key=True)
)

# 用户m:n用户（关注与被关注）
tb_user_follow = db.Table(
    'tb_user_follow',
    db.Column('origin_user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True),
    db.Column('follow_user_id', db.Integer, db.ForeignKey('user_info.id'), primary_key=True)
)


# 用户
class UserInfo(db.Model, BaseModel):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(50), default='user_pic.png')
    nick_name = db.Column(db.String(20))
    signature = db.Column(db.String(200))
    public_count = db.Column(db.Integer, default=0)
    follow_count = db.Column(db.Integer, default=0)
    mobile = db.Column(db.String(11))
    password_hash = db.Column(db.String(200))
    gender = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)

    # 用户与发布新闻的关系
    news = db.relationship('NewsInfo', backref='user', lazy='dynamic')
    # 用户与评论的关系user.comments,comment.user
    comments = db.relationship('NewsComment', backref='user', lazy='dynamic')
    # 用户与收藏新闻的关系（多对多，依赖关系表）
    news_collect = db.relationship(
        'NewsInfo',
        secondary=tb_news_collect,
        lazy='dynamic'
    )
    # 用户与关注用户的关系（多对多，依赖关系表）
    follow_user = db.relationship(
        'UserInfo',
        secondary=tb_user_follow,
        lazy='dynamic',
        # 自关联user.follow_user-->primaryjoin-->当前用户user关注了哪些用户
        primaryjoin=id == tb_user_follow.c.origin_user_id,
        # user.follow_by_user==>secondaryjoin-->当前用户user被哪些用户关注
        secondaryjoin=id == tb_user_follow.c.follow_user_id,
        backref=db.backref('follow_by_user', lazy='dynamic')
    )

    @property
    def password(self):
        pass

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    @property
    def avatar_url(self):
        url = current_app.config.get('QINIU_URL')
        return url + self.avatar


# 新闻１：ｎ新闻评论, 新闻评论1:n用户, 用户评论１: n用户评论
class NewsComment(db.Model, BaseModel):
    __tablename__ = 'news_comment'
    id = db.Column(db.Integer, primary_key=True)
    like_count = db.Column(db.Integer, default=0)
    msg = db.Column(db.String(200))
    news_id = db.Column(db.Integer, db.ForeignKey('news_info.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('news_comment.id'))
    comments = db.relationship('NewsComment', lazy='dynamic')