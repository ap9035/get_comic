# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os
import sys
import multiprocessing

img_regex = re.compile(r'(http.{,50}\d\d\d.jpg)')
page_regex=re.compile(r'value="(\d+).html')

def download_pic(pic_url, dir):
    try:
        pic_name = dir + '/' + pic_url.split('/')[-1]
        urllib.urlretrieve(pic_url, pic_name)
    except IOError as ioerr:
        print "IOError in download picture: " + pic_url

def get_page_list(url_content):
	parse_start = url_content.find('option selected')
	parse_end = url_content.find('http://img.cartoonmad.com/image/rad.gif')
	page_list= page_regex.findall(url_content[parse_start-1:parse_end])
	return page_list

def get_pic_url(url_content):
	parse_start = url_content.find('<td align="center">')
	parse_end = url_content.find('border="0" oncontextmenu')
	img_url = img_regex.findall(url_content[parse_start-1:parse_end])
	return img_url[0]

def store_pic(url,dir_name):
	try:
		content = urllib2.urlopen(url).read()
	except urllib2.HTTPError as httperr:
		print "urllib2.HTTPError detected in store_pic():" + url
		return
	except urllib2.URLError as urlerr:
		print "URLError detected in store_pic(): " + url
		return
	pic_url	=	get_pic_url(content)

	if not os.path.exists(dir_name):
	        try:
			os.mkdir(dir_name)
		except OSError as err:
			print err, url
	
	download_pic(pic_url,dir_name)

def get_comic(url,dir_name):
	try:
		content = urllib2.urlopen(url).read()
	except urllib2.HTTPError as httperr:
		print "urllib2.HTTPError detected in store_pic():" + url
		return
	except urllib2.URLError as urlerr:
		print "URLError detected in store_pic(): " + url
		return
	
	page_list=	get_page_list(content)
	iter=1
	for i in page_list:
		url="http://web.cartoonad.com/comic/"+i
		p=multiprocessing.Process(target=store_pic,args=(url,dir_name))
		p.start()
		iter+=1

def main():
	url=sys.argv[1]
	dir_name=sys.argv[2]
	get_comic(url,dir_name)

if __name__ == '__main__':
	main()
