import re
import scraperwiki
import requests
from lxml.html.soupparser import fromstring
from time import sleep

month = "Oct 17"

def search(mth):
#  	request_data = { "searchCriteria.parish": ALL, "searchCriteria.ward": ALL, "month": mth, "dateType": "DC_Validated" , "searchType": "Application" }

  	request_data = {"month": mth, "dateType": "DC_Validated" , "searchType": "Application" }

	# <input type="radio" name="dateType" value="DC_Validated" checked="checked" id="dateValidated">
    
	sleep(2)
	result = requests.post('http://public.oxford.gov.uk/online-applications/monthlyListResults.do?action=firstPage', request_data)

	if not result:
		print "No result returned"
		return
	
	result_dom = fromstring(result.content)
  
  	results = result_dom.xpath("//li[@class='searchresult'")
  	print len(results)
	

search(month)
