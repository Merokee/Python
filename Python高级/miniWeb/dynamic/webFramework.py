import re
g_path_method = {}
from pymysql import *
from urllib import parse


class PythonMysql(object):
    def __init__(self):
        self.conn = connect(host="localhost", port=3306, database="stock_project", user="root", password="mysql", charset="utf8")
        self.cur = self.conn.cursor()

    def select(self, sql, arg_list=None):
        count = self.cur.execute(sql, arg_list)
        return count, self.cur.fetchall()

    def update(self, sql, arg_list=None):
        self.cur.execute(sql, arg_list)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()


pm = PythonMysql()


def route(keyWord):
    def decorator(func):
        g_path_method[keyWord] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return decorator


@route(r"/index.html")
def get_index(*args):
    with open("./templates/index.html") as f:
        content = f.read()
    html_templates = """<tr>
                           <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>
                                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
                            </td>
                        </tr>"""
    sql = "select * from info"
    count, data = pm.select(sql)
    html = "" 
    for item in data:
        html += html_templates % (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[1])
    content = re.sub(r"\{%content%\}", html, content)
    return content


@route(r"/center.html")
def get_center(*args):
    with open("./templates/center.html") as f:
        content = f.read()
    html_templates ="""<tr>
                           <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                           <td>
                               <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                           </td>
                           <td>
                               <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                           </td>
                       </tr>"""
    sql = "select i.code, i.short, i.chg, i.turnover, i.price, i.highs, note_info from info as i inner join focus as f on i.id=f.info_id "
    count, data = pm.select(sql)
    html = ""
    for item in data:
        html += html_templates % (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[0], item[0])
    content = re.sub(r"\{%content%\}", html, content)
    return content


@route(r"/add/([\d]{6})\.html")
def add_foucs(*args):
    pattern, keyWord = args[0], args[1]
    stock_code = re.match(pattern, keyWord).group(1)
    sql = "select * from focus where info_id = (select id from info where code = %s)"
    count, focus_info = pm.select(sql, arg_list=[stock_code])
    if count >0:
        return "已关注，请勿重复关注！"
    sql = "insert into focus (info_id) select id from info where code = %s"
    pm.update(sql, arg_list= [stock_code])
    return "关注成功"


@route(r"/del/(.*)\.html")
def cancle_focus(*args):
    pattern, keyWord = args[0], args[1]
    stock_code = re.match(pattern, keyWord).group(1)
    sql = "delete from focus where info_id = (select id from info where code = %s)"
    pm.update(sql, arg_list= [stock_code])
    return "取关成功！"


@route(r"/update/([\d]{6})\.html")
def update(*args):
    pattern, keyWord = args[0], args[1]
    stock_code = re.match(pattern, keyWord).group(1)
    with open("./templates/update.html", "r") as f:
        content = f.read()
    content = re.sub(r"\{%code%\}", stock_code, content)
    sql = "select note_info from focus where info_id = (select id from info where code = %s)"
    count, note_info = pm.select(sql, [stock_code])
    print(count, note_info)
    content = re.sub(r"\{%note_info%\}", note_info[0][0], content)
    return content

@route(r"/update/([\d]{6})/(.*)\.html")
def update_note_info(*args):
    pattern, keyWord = args[0], args[1]
    stock_code = re.match(pattern, keyWord).group(1)
    note_info = re.match(pattern, keyWord).group(2)
    note_info = parse.unquote(note_info)
    sql = "update focus set note_info = %s where info_id = (select id from info where code = %s)"
    pm.update(sql, [note_info, stock_code])
    return "修改成功！"


def application(environ, start_response):
    status = "200 OK"
    response_headers = [("Content-Type", "text/html;charset=utf-8")]
    start_response(status, response_headers)
    keyWord = environ["PATH_INFO"]
    print(keyWord, "*"*30)
    for key, value in g_path_method.items():
        ret = re.match(key, keyWord)
        if ret:
            return value(key, keyWord)
    else:
        return "你请求的url:%s尚未实现" % keyWord
