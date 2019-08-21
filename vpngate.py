import urllib.request
import re

from bs4 import BeautifulSoup

root_url = "http://185.210.217.34:57406/cn/"

# 请求

# response=urllib.request.urlopen('http://www.baidu.com')

# http://37.120.154.37:23010
# http://185.210.217.34:57406
# http://95.183.48.124:20893
# 创建Request对象
request = urllib.request.Request(root_url)
# 添加数据
# request.data = 'a'
# 添加http的header #将爬虫伪装成Mozilla浏览器
request.add_header('User-Agent', 'Mozilla/5.0')
# 添加http的header #指定源网页，防止反爬
request.add_header('Origin', 'https://www.baidu.com')
# 发送请求获取结果
# response = urllib.request.urlopen(request)

fhandle=open("./vpngate.html",encoding='utf8')
# print(fhandle.read().encode('GBK', 'ignore'))
soup = BeautifulSoup(
    fhandle.read().encode('GBK', 'ignore'),            # HTML文档字符串
    'html5lib',         # HTML解析器
    from_encoding='utf8'  # HTML文档的编码
)

# 解析

# 第一步：根据HTML网页字符串创建BeautifulSoup对象
# soup = BeautifulSoup(
#     response.read(),        # HTML文档字符串
#     'html.parser',        # HTML解析器
#     from_encoding='utf8'  # HTML文档的编码
# )
# 第二步：搜索节点（find_all,find）
# 方法：find_all(name,attrs,string)    # 名称,属性,文字
# 查找所有标签为a的标签
# links = soup.find_all('a')
# 查找第一个标签为a的标签
# soup.find('a')
# 查找所有标签为a,链接符合'/view/123.html'形式的节点
# soup.find_all('a',href='/view/123.html')
# 查找所有标签为div,class为abc，文字为python的节点
# soup.find_all('div',class_='abc',string='python')
# class 是 Python 保留关建字，所以为了区别加了下划线

table = soup.find_all("table" , {"id":"vg_hosts_table_id"})[2]
rows = table.find_all("a",{"href":re.compile(r"do_openvpn.aspx\?fqdn=(\w+)?")})
for row in rows:
    detail_url = root_url + row["href"]
    detail_page = urllib.request.urlopen(detail_url)
    detail_soup = BeautifulSoup(detail_page.read(),'html5lib',from_encoding='utf8')
    # down_urls = detail_soup.find_all("a",{"href":re.compile(r"\/common\/openvpn_download.aspx(\w+)?")})
    down_urls = detail_soup.find_all("a")
    for down_url in down_urls:
    	print(down_url["href"])


# data=response.read()    # read all

# dataline=response.readline()    # read line

# fhandle=open("./1.html","wb")    # save local
# fhandle.write(data)
# fhandle.close()
