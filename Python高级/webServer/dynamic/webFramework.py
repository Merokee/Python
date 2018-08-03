# web框架
from pymysql import * 
import re
dict1 = {}


class PythonMysql(object):
    def __init__(self):
        self.conn = connect(host="localhost", port=3306, database="stock_project", user="root", password="mysql", charset="utf8")
        self.cur = self.conn.cursor()

    def exe(self, sql):
        count = self.cur.execute(sql)
        return count

    def select(self, sql):
        self.exe(sql)
        return self.cur.fetchall()

    def update(self, sql):
        self.exe(sql)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()


pm = PythonMysql()


def extral(file_name):
    def decorate(func):
        dict1[file_name] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return decorate


@extral("/index.html")
def index():
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
                                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007">
                            </td>
                        </tr>"""
    sql = "select * from info"
    data = pm.select(sql)
    html = "" 
    for item in data:
        html += html_templates % (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
    content = re.sub(r"\{%content%\}", html, content)
    return content


@extral("/center.html")
def center():
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
                               <a type="button" class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                           </td>
                           <td>
                               <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="300268">
                           </td>
                       </tr>"""
    sql = "select i.code, i.short, i.chg, i.turnover, i.price, i.highs, note_info from info as i inner join focus as f on i.id=f.info_id "
    data = pm.select(sql)
    html = ""
    for item in data:
        html += html_templates % (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
    content = re.sub(r"\{%content%\}", html, content)
    return content


def app(env, start_response):
    status = "200 OK"
    response_headers = [("Content-Type", "text/html;charset=utf-8")]
    file_name = env["PATH_INFO"]
    method = dict1.get(file_name)
    if method:
        content = method()
    else:
        status = "404 Not Found"
        content = "404 Not Found, 文件没有找到!" 
    start_response(status, response_headers)
    return content
