#!/usr/local/sbin/python
import urllib2

def downloader(urls):
	html = []

	for x in urls:
		source = urllib2.urlopen(x)
		html.append( source.read() ) 
		source.close()

	return html

url1 = "http://mysql12.f4.htw-berlin.de/crawl/d01.html"
url2 = "http://mysql12.f4.htw-berlin.de/crawl/d06.html"
url3 = "http://mysql12.f4.htw-berlin.de/crawl/d08.html"
urls = [url1, url2, url3]

pages = downloader(urls)

for k in pages:
		print k