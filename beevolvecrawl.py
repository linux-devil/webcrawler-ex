import urllib
import re,csv,string
def find_nth(s, x, n):
    i = -1
    for _ in range(n):
        i = s.find(x, i + len(x))
        if i == -1:
            break
    return i
def add_data(name, phone, website):
	datum = [name,phone,website]
	writer = csv.writer(open("firms.csv",'ab'), delimiter= '\t',quoting=csv.QUOTE_MINIMAL) 
	writer.writerow(datum)
	return True
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
	url = mainurl+each_line
	page = urllib.urlopen(url)
	text = page.read()
	s= "verdananocolor14pxbold"
	len2 = len(s)
	len1=  find_nth(text, s, 2)
	len3 = len1+len2+2
	t = text[len3:]
	name = t[:t.find("<")]
	webpoint = t.find("http://")
	raw = t[:webpoint]
	webaddr = t[webpoint:]
	webaddress = webaddr[:webaddr.find("\"")]
	if(len(webaddress)<40):
		weby = webaddress
	else:
		weby = "null"
	phonepattern = re.compile(r"(\d{3})\D*(\d{3})\D*(\d{4})")
	iterator = phonepattern.finditer(raw)
	t= ()
	for match in iterator:
		t =match.span()
		if(t[1]-t[0] == 12):
			phone = match.group()
			break;
		else:
			phone = "null"
	add_data(name,phone,weby)	
