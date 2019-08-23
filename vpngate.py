import urllib.request
import http.cookiejar
import re
import os
from bs4 import BeautifulSoup


'''
需要安装
pip install beautifulsoup4
pip install html5lib
'''
class Vpngate(object):

    def __init__(self, host):
        self.protocol = "http://"
        self.host = host

    def download_config(self,path):
    	home_url = self.protocol + self.host + "/cn/"
    	detail_urls = self.__parse_detail_url(self.__http_get(home_url).read())
    	for detail_url in detail_urls:
    		down_urls = self.__parse_down_url(self.__http_get(self.protocol+detail_url))
    		for down_url in down_urls:
    			file_url = self.protocol + down_url
    			file_name = file_url.split('/')[-1]
    			if not os.path.exists(path):
    				os.makedirs(path)
    			urllib.request.urlretrieve(file_url, filename=path+"/"+file_name)


    def __http_get(self,url):
    	request = urllib.request.Request(url)
    	request.add_header('User-Agent', 'Mozilla/5.0')
    	request.add_header('Origin', 'https://www.baidu.com')
    	response = urllib.request.urlopen(request)
    	return response


    def __parse_detail_url(self,html):
    	soup = BeautifulSoup(html,'html5lib',from_encoding='utf8')
    	table = soup.find_all("table" , {"id":"vg_hosts_table_id"})[2]
    	rows = table.find_all("a",{"href":re.compile(r"do_openvpn.aspx\?fqdn=(\w+)?")})
    	return map(lambda row:self.host + "/cn/"+row["href"], rows)


    def __parse_down_url(self,html):
    	soup = BeautifulSoup(html,'html5lib',from_encoding='utf8')
    	down_urls = soup.find_all("a",{"href":re.compile(r"/common/openvpn_download.aspx\?sid=(\d+)&udp=(\d+)&host=[\d\.]+(\w+)?")})
    	return map(lambda url:self.host + url["href"],down_urls)