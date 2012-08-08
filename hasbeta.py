import re,csv,string
import urllib,urllib2
from HTMLParser import HTMLParser
from HTMLParser import *
def add_data(name, phone, website):
	datum = [name,phone,website]
	writer = csv.writer(open("firms.csv",'ab'), delimiter= '\t',quoting=csv.QUOTE_MINIMAL) 
	writer.writerow(datum)
	return True

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.recording= 0
		self.data = []
	def handle_starttag(self,tag,attrs):
		if tag == 'td':
			for name, value in attrs:
				if name == 'width' and value == '610':
					self.recording = 1
	def handle_endtag(self, tag):
		if tag == 'td' and self.recording:
			self.recording -=1 
	def handle_data(self, data):
		if self.recording:
			self.data.append(data)
p = re.compile('prid')
mainurl = "http://www.odwyerpr.com/pr_firms_database/"
dbfile = file('depth_1.txt','wt')
for i in re.findall('''href=["'](.[^"']+)["']''',urllib.urlopen("http://www.odwyerpr.com/pr_firms_database/index.htm").read(),re.I):
	if(i.find('prid=') != -1):
		print(i)
		dbfile.write(i +'\n')
dbfile.close()
lol = open("depth_1.txt")
for each_line in lol:
	p = MyHTMLParser()	
	url = mainurl+each_line
	if(url[65]=='{'):
		f = urllib2.urlopen(url)
		try:
			html = f.read()
			if(html.find('logos')== -1):
				p.feed(html)
				raw = ''.join(p.data)
				name = p.data[1]
				phone = p.data[3].replace(';','').split()
				t = raw[raw.find("www."):]
				webaddress = t[:t.find(" ")]
				l = re.split('[\s"]+',string.strip(webaddress))
				p.close()
				try:
					add_data(name,phone[0],l[0])
				except:
					add_data(name,"null",l[0])
			else:
				p.feed(html)
				raw = ''.join(p.data)
				name = p.data[2]
				phone = p.data[4].replace(';','').split()
				t = raw[raw.find("www."):]
				webaddress = t[:t.find(" ")]
				l = re.split('[\s"]+',string.strip(webaddress))
				p.close()
				
		except HTMLParseError:
			pass
		
	else:
		f = urllib2.urlopen(url)
		try:		
			html = f.read()
			if(html.find('logos')!= -1):
				p.feed(html)
				name= p.data[2]
				raw = ''.join(p.data)
				phone = p.data[4].replace(';','').split()
				t = raw[raw.find("www."):]
				webaddress = t[:t.find(" ")]
				l = re.split('[\s"]+',string.strip(webaddress))
				try:
					add_data(name,phone[0],l[0])
				except:
					add_data(name,"null",l[0])
			
			else:
				p.feed(html)
				name= p.data[1]
				raw = ''.join(p.data)
				phone = p.data[3].replace(';','').split()
				t = raw[raw.find("www."):]
				webaddress = t[:t.find(" ")]
				l = re.split('[\s"]+',string.strip(webaddress))
				try:
					add_data(name,phone[0],l[0])
				except:
					add_data(name,"null",l[0])
		except HTMLParseError:
			pass	
