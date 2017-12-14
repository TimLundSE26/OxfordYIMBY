import re
import scraperwiki
import requests
from lxml.html.soupparser import fromstring
from time import sleep

month = "Oct 17"

def search(mth):
  	request_data = { "month": mth, "dateType": "DC_Validated" }

	# <input type="radio" name="dateType" value="DC_Validated" checked="checked" id="dateValidated">
# is this the way to pass values when posting to a form? A dictionary object with the keys being the names of the controls?
    
	print "POST 'http://public.oxford.gov.uk/online-applications/advancedSearchResults.do?action=firstPage'"
	sleep(2)
	result = requests.post('http://public.oxford.gov.uk/online-applications/search.do?action=monthlyList', request_data)

	result_dom = fromstring(result.content)

	applications = result_dom.xpath("//li[@class='searchresult']")

	if len(applications) == 0:
		return
	else:
		for index, application in enumerate(applications):
			application_link = application.xpath("a/@href")
			matchObj = re.search( r'keyVal=(.*$)', application_link)
			key = matchObj.group(1)

			tabletype = "summary"            
			application_url = "http://public.oxford.gov.uk/online-applications/applicationDetails.do?activeTab=" + tabletype + "&keyVal=" + key
			application_url = "http://public.oxford.gov.uk" + application_link
			print "GET " + application_url

			sleep(2)
			application_page = requests.get(application_url)
			application_dom = fromstring(application_page.content)    

			print len(application_dom.xpath("//table"))
            
search(month)
