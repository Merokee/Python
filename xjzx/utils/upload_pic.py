# -*- coding: utf-8 -*-
# flake8: noqa
from flask import current_app
from qiniu import Auth, put_data


def upload_pic(f1):
    #需要填写你的 Access Key 和 Secret Key
    access_key = current_app.config.get('QINIU_AK')
    secret_key = current_app.config.get('QINIU_SK')

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = current_app.config.get('QINIU_BUCKET')

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)

    # f1表示接收的浏览器传递的文件对象
    ret, info = put_data(token, None, f1.read())

    return ret.get('key')



