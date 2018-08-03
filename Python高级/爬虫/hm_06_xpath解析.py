from lxml import etree
html_str = """<html>
	<head>

		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<meta http-equiv="content-type" content="text/html;charset=utf-8">
		<meta content="always" name="referrer">
        <meta name="theme-color" content="#2932e1">
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <link rel="icon" sizes="any" mask href="//www.baidu.com/img/baidu_85beaf5496f291521eb75ba38eacbd87.svg">
        <link rel="search" type="application/opensearchdescription+xml" href="/content-search.xml" title="百度搜索" />


<title>苹果_百度搜索</title>"""
# 加载网页字符串
# html_obj = etree.HTML(html_str)
# result = html_obj.xpath("//meta/@content")
# print(result)

# 加载网页文件 必须设置解析器
parser = etree.HTMLParser()
html_obj = etree.parse("baidu.Html", parser)

# 使用xpath进行解析 xpath返回的一定是列表
result = html_obj.xpath("//title/text()")
print(result)