import re
import scraperwiki
import requests
from lxml.html.soupparser import fromstring
from time import sleep

month = "Oct 17"

def search(mth):
	
  	request_data = {"month": mth, "dateType": "DC_Validated" , "searchType": "Application" }
	sleep(2)
	result = requests.post('http://public.oxford.gov.uk/online-applications/monthlyListResults.do?action=firstPage', request_data)
	
	if not result:
		print "No result returned"
		return
	
	result_dom = fromstring(result.content)  
  	applications = result_dom.xpath("//li[@class='searchresult']")
  	print len(applications)
	
	for application in applications:
		link = "".join(application.xpath('a/@href')).strip()
		description = "".join(application.xpath('a/text()')).strip()
		address = "".join(application.xpath('p[@class="address"]/text()')).strip()
		meta = "".join(application.xpath('p[@class="metaInfo"]/text()')).strip()
		
		print link, address
	
	sleep(2)
	result = requests.get('http://public.oxford.gov.uk/online-applications/pagedSearchResults.do?action=page&searchCriteria.page=2')
	
	result_dom = fromstring(result.content)  
  	applications = result_dom.xpath("//li[@class='searchresult']")
  	print len(applications)
	
	for application in applications:
		link = "".join(application.xpath('a/@href')).strip()
		description = "".join(application.xpath('a/text()')).strip()
		address = "".join(application.xpath('p[@class="address"]/text()')).strip()
		meta = "".join(application.xpath('p[@class="metaInfo"]/text()')).strip()
		
		print link, address
		
	
#	iPage = 2
#	request_data = {"searchCriteria.page": "2", "action": "page", "orderBy": "DateReceived", "orderByDirection": "Ascending", "searchCriteria.resultsPerPage": "10"}
	
#	sleep(2)
#	result = requests.post('http://public.oxford.gov.uk/online-applications/pagedSearchResults.do', request_data)
#	result_dom = fromstring(result.content)  
 # 	results = result_dom.xpath("//li[@class='searchresult']")
  #	print len(results)
	
search(month)
