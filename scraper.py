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
  	results = result_dom.xpath("//li[@class='searchresult']")
  	print len(results)
	
	for result in results:
		link = "".join(result.xpath('a/@href')).strip()
		description = "".join(result.xpath('a/text()')).strip()
		address = "".join(result.xpath('p[@class="address"]/text()')).strip()
		meta = "".join(result.xpath('p[@class="metaInfo"]/text()')).strip()
		
		print link, meta
		
#	iPage = 2
#	request_data = {"searchCriteria.page": "2", "action": "page", "orderBy": "DateReceived", "orderByDirection": "Ascending", "searchCriteria.resultsPerPage": "10"}
	
#	sleep(2)
#	result = requests.post('http://public.oxford.gov.uk/online-applications/pagedSearchResults.do', request_data)
#	result_dom = fromstring(result.content)  
 # 	results = result_dom.xpath("//li[@class='searchresult']")
  #	print len(results)
	
search(month)
