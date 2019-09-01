from requests_html import HTMLSession
import demjson
import re, json
from pprint import pprint

from urllib.parse import urlparse

rx = re.compile(r'(?<=var videoarrayoj =)[^;]+')
# rx = re.compile(r'(?<=var videoarrayoj)(?:[^\=+)([^;]+)')
# rx = re.compile(r'(?<=var videoarrayoj)(?:[^\[]+)([^;]+)')

class Jav(HTMLSession):# HEADERS = {'host':'javfor.me'}
	def get_vars(self, soup):
		scripts = soup('script')
		for i in scripts:
			i = i.text
			# i = i.string
			if not i or 'videoarrayoj' not in i:continue
			for x in i.split('\t'):
				x = re.search(rx, x)
				if not x:continue
				x = x.group()
				# print(x)
				x = demjson.decode(x)
				x = {o['servername']:map(lambda l:f'http://l1.jav4.me/sembed.php?{l}', json.loads(o['links'])) for o in x}
				return x
			print('Not found')

	def fetch(self, url, **kwargs):
		url = url.strip()
		try:
			req = self.get(url, **kwargs)
		except:
			print('CONNECT ERROR')
			exit()
		soup = req.html
		print(soup.find('title', first=1).text)
		links = sorted(self.get_vars(soup.find).items(), 
			key=lambda x:x[0] and x[0].lower().find('gg'),
			reverse=True)
		urls = set()
		for server, i in links:
			if i == 'UE':continue
			# # if i != 'GG':continue
			a = ''
			for o in i:
			# 	# print(o)
				url = self.get(o).html.find('source', first=1).attrs['src']
				parse = urlparse(url)
				if not parse.scheme:continue
				urls.add(parse.netloc)
				# if url.startswith('//'):
				# 	url = 'http:'+url
				print(url)
				o = int(self.head(url).headers['Content-Length'])//(1024**2)
				a+= '\n'
				a+= str(o) if o else ''
			a+= '\n'
			print(a)
			# if server == 'GG':break
			# break
		for i in urls:
			# print(i.scheme)
			print(i)

# 
# http://javfor.me/42436.html
# http://javfor.me/36842.html
j = Jav()
# http://javfor.me/88778.html
# http://javfor.me/66562.html
# http://javfor.me/90828.html
# http://javfor.me/90543.html
j.fetch('''
http://javfor.me/96097.html#
''', )
# gen = j.fetch('http://javfor.me/101980.html', 
	# proxies={}
	
# exit()
# def parse_link(items):
# 	items = demjson.decode(items)
# 	return {item['servername']:[ get_video_link(i) for i in json.loads(item['links'])] for item in items}
