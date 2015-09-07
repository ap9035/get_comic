# -*- coding: UTF-8 -*-
import urllib
import urllib2
import re
import os
import sys
import multiprocessing
import get_comic

page_regex=re.compile(r'href=(/comic/\d{15}.html)')
name_regex=re.compile(r'href=/comic/\d{15}.html target=_blank>(....)\n.+(\d\d\d.+)</a>')

def get_page_list(url_content):
	parse_start = url_content.find('<html>')
	parse_end = url_content.find('</html>')
	page_list= page_regex.findall(url_content[parse_start-1:parse_end])
	return page_list

def get_name_list(url_content):
	parse_start = url_content.find('<html>')
	parse_end = url_content.find('</html>')
	name_list= name_regex.findall(url_content[parse_start-1:parse_end])
	ret_var=[]
	for i in name_list:
		ret_var.append((i[0]+i[1]).decode('big5').encode('utf8'))
	return ret_var

def main():
	url=sys.argv[1]
	mdir=sys.argv[2]
	print mdir

	try:
		content = urllib2.urlopen(url).read()
	except urllib2.HTTPError as httperr:
		print "urllib2.HTTPError detected in store_pic():" + url
		return
	except urllib2.URLError as urlerr:
		print "URLError detected in store_pic(): " + url
		return

	page_list	=	get_page_list(content)
	name_list	=	get_name_list(content)
	iter=1

	for i in page_list:
		url="http://www.cartoonmad.com/"+i
		dir_name=mdir+name_list[iter-1];
		print dir_name," store"
		get_comic.get_comic(url,dir_name)
		iter+=1		
			
if __name__ == '__main__':
	main()
