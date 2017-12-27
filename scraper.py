import re
import scraperwiki
import requests
from lxml.html.soupparser import fromstring
from time import sleep

month = "Oct 17"
laurlroot = "http://planning.lewisham.gov.uk"

def search(mth):
#	session = requests.Session()
	
  	request_data = {"month": mth, "dateType": "DC_Validated" , "searchType": "Application" }
	
	sleep(2)
#	result = session.post(laurlroot + '/online-applications/monthlyListResults.do?action=firstPage', request_data)
	result = requests.post(laurlroot + '/online-applications/monthlyListResults.do?action=firstPage', request_data)
	
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
#	result = session.get(laurlroot + '/online-applications/pagedSearchResults.do?action=page&searchCriteria.page=2')
	
#	result_dom = fromstring(result.content)  
#  	applications = result_dom.xpath("//li[@class='searchresult']")
#  	print len(applications)

	
#searchCriteria.page="n"
#action" value="page"

# this is a guess at what data to post
#	request_data = {"month": mth, 
#			"dateType": "DC_Validated" , 
#			"searchType": "Application", 
#			"searchCriteria.page": "2" , 
#			"action": "page",
#		        "searchCriteria.resultsPerPage": "5"}
	
#	sleep(2)
	

#	result = session.post(laurlroot + '/online-applications/pagedSearchResults.do', request_data)
	
#	if not result:
#		print "No result returned for second post"
#		return
	
#	result_dom = fromstring(result.content)  
 # 	applications = result_dom.xpath("//li[@class='searchresult']")
  #	print len(applications)	
	
#	for application in applications:
#		link = "".join(application.xpath('a/@href')).strip()
#		description = "".join(application.xpath('a/text()')).strip()
#		address = "".join(application.xpath('p[@class="address"]/text()')).strip()
#		meta = "".join(application.xpath('p[@class="metaInfo"]/text()')).strip()
		
#		print link, address
		

	
search(month)
