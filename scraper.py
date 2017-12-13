import re
import scraperwiki
import requests
from lxml.html.soupparser import fromstring
from time import sleep

def search():
	print "GET 'http://mycouncil.oxford.gov.uk/mgMemberIndex.aspx?FN=ALPHA&VW=TABLE&PIC=1'" 
	sleep(2)
	result = requests.get('http://mycouncil.oxford.gov.uk/mgMemberIndex.aspx?FN=ALPHA&VW=TABLE&PIC=1')
	result_dom = fromstring(result.content)
	councillors = result_dom.xpath("//table[@id='mgTable1']//tr")
	
	print len(councillors)
	
	councillor = councillors[0]
	col1 = councillor.xpath("td")[1].strip()
	
	print col1
	
#	if len(councillors) == 0:
#		return
#	else:
#		for index, councillor in enumerate(councillors):
#			col1 = councillor.xpath(".//td)[1]").strip()
#			data = {"col1": col1, "index": index}
			
#			print data
#			scraperwiki.sqlite.save(unique_keys=['index'], data=data)
		

search()
