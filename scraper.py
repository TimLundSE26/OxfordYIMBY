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
	
# GET on the url with searchCriteria.page=N ...
#	result = requests.get('http://public.oxford.gov.uk/online-applications/pagedSearchResults.do?action=page&searchCriteria.page=2')
	
#	result_dom = fromstring(result.content)  
#  	applications = result_dom.xpath("//li[@class='searchresult']")
#  	print len(applications)

	#doesn't seem to work
	
# David suggests "There is doubtless a way to handle the cookies in Python (it's been a while, so I don't have the 
#    answer in my head right now), but the good news is that they don't seem to be necessary - submitting the same POST
#    request without them still gets the desired results.
	
#searchCriteria.page="n"
#action" value="page"

# this is a guess at what data to post
	request_data = {"month": mth, 
			"dateType": "DC_Validated" , 
			"searchType": "Application", 
			"searchCriteria.page": "2" , 
			"action": "page",
		        "searchCriteria.resultsPerPage": "5"}
	
	sleep(2)
	

	result = requests.post('http://public.oxford.gov.uk/online-applications/pagedSearchResults.do', request_data)
	
	if not result:
		print "No result returned for second post"
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
		

	
search(month)
