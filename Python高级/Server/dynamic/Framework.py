functionDict = {}
import re


def route(reFunc):
    def decorator(func):
        print(reFunc)
        functionDict[reFunc] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return decorator


def update(*args, **kwargs):
    with open("templates/update.html", "r")as f:
        content = f.read()
    return content


@route(r"/center.html")
def center(*args, **kwargs):
    with open("templates/center.html", "r") as f:
        content = f.read()
    return content


@route(r"/index.html")
def index(*args, **kwargs):
    with open("templates/index.html", "r") as f:
        content = f.read()
    return content


def application(env, start_response):
    fileName = env["PATH_INFO"]
    headers = [("Content-Type", "text/html;charset=utf-8")]
    print("走到这一步"*8)
    print(functionDict)
    for reFunc, func in functionDict.items():
        print(reFunc, func, "---"*30)
        ret = re.match(reFunc, fileName)
        print(">>>"*30, ret)
        if ret:
            status = "200 OK"
            start_response(status, headers)
            return func(fileName, reFunc)
    else:
        status = "404 Not Found"
        response_body = "404 Not Found"
        start_response(status, headers)
        return response_body