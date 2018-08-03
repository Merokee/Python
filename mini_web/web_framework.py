import re
from pymysql import *
import urllib.parse

g_template_path = './templates'
add_pattern = r"/add/(\d{6})\.html"
update_pattern = r"/update/(\d{6})\.html"
update_info_pattern = r"/update/(.*)/(.*)\.html"

def index(file_path):
    f = open(g_template_path + file_path)
    content = f.read()
    f.close()

    conn = connect(host='localhost', port=3306, database='stock_project', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql = "select * from info"
    cur.execute(sql)
    ret = cur.fetchall()
    # 遍历获取查询的数据
    html_template = """<tr>
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
    html = ""
    for item in ret:
        html += html_template % (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[1])

    cur.close()
    conn.close()
    # 在模板添加动态数据
    # html = "<h1>首页数据: 这里是从mysql数据库中读取的动态数据</h1>"
    # 完成数据的替换
    content = re.sub(r"\{%content%\}", html, content)
    return content

def update_page(path):

    # 根据正则表达式 在path 路径中提取股票的code码
    ret = re.match(update_pattern, path)
    code = ret.group(1)
    f = open(g_template_path + "/update.html", encoding="utf-8")
    content = f.read()
    f.close()

    conn = connect(host='localhost', port=3306, database='stock_project', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql = "select i.short, f.note_info from info as i inner join focus as f on i.id = f.info_id where i.code = %s"
    cur.execute(sql, [code])
    ret = cur.fetchone()
    cur.close()
    conn.close()
    # 获取名字和 描述信息
    short = ret[0]
    note_info = ret[1]


    # 根据code码获取股票的名字和描述信息
    content = re.sub(r"\{%code%\}",short,content)
    content = re.sub(r"\{%note_info%\}", note_info, content)
    # 完成数据的替换
    # 返回数据
    return content

def update_info(path):
    # /update/%E5%8D%97%E9%80%9A%E9%94%BB%E5%8E%8B/%E4%BD%A0%E5%A5%BD.html
    # 提取股票简称 和 备注的信息
    ret = re.match(update_info_pattern, path)
    short = ret.group(1)
    note_info = ret.group(2)

    # 对提取的信息 做url解码
    short = urllib.parse.unquote(short)
    note_info = urllib.parse.unquote(note_info)
    print(short, "+++++++++++", note_info)
    # 打开数据库的连接
    conn = connect(host='localhost', port=3306, database='stock_project', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql = "update focus set note_info = %s where info_id = (select id from info where short = %s)"
    # 操作数据
    cur.execute(sql, [note_info, short])
    conn.commit()
    cur.close()
    conn.close()
    return "修改成功"


def add(path):

    ret = re.match(add_pattern, path)
    code = ret.group(1)

    # 想focus表中插入数据
    conn = connect(host='localhost', port=3306, database='stock_project', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    # 已知code 获取 对应的id
    # insert select

    # 判断是否已经被关注
    # 标量子查询
    sql = "select * from focus where info_id = (select id from info where code = %s)"
    cur.execute(sql, [code])
    ret = cur.fetchone()
    if ret:
        # 已经关注
        return "已经关注了该股票, 请不要重复关注"

    sql = "insert into focus (info_id) select id from info where code = %s"
    cur.execute(sql, [code])
    # 数据的更新
    conn.commit()

    cur.close()
    conn.close()
    return "关注股票成功 %s" % code

def center(file_path):
    f = open(g_template_path + file_path, encoding="utf-8")
    content = f.read()
    f.close()
    # 连接数据库获取数据
    conn = connect(host='localhost', port=3306, database='stock_project', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql = "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id = f.info_id"
    cur.execute(sql)
    ret = cur.fetchall()
    # 遍历获取查询的数据
    html_template = """<tr>
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
    html = ""
    for item in ret:
        html += html_template % (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[0], item[0])

    cur.close()
    conn.close()
    # 在模板添加动态数据
    # html = "<h1>首页数据: 这里是从mysql数据库中读取的动态数据</h1>"
    # 完成数据的替换
    content = re.sub(r"\{%content%\}", html, content)
    return content


def application(environ, start_response):
    """
    web框架和web服务器交互的接口方法
    :param file_name: 需要访问的动态资源
    :param start_response: 在web服务器中定义方法的引用, 需要在框架中执行, 将拼接好的请求头传递方web服务器
    :return: 返回获取的动态内容
    """
    path_info = environ["PATH_INFO"]
    status = "200 OK"
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    if path_info == "/index.html":
        return index(path_info)
    if path_info == '/center.html':
        return center(path_info)
    if re.match(add_pattern,path_info) is not None:
        return add(path_info)
    if re.match(update_pattern,path_info) is not None:
        return update_page(path_info)
    if re.match(update_info_pattern,path_info) is not None:
        return update_info(path_info)
    else:
        return "sorry, not found,没有对应的路径"