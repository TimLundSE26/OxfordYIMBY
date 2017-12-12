import re
import scraperwiki
import requests
from lxml.html.soupparser import fromstring
from time import sleep

wards = ["BARTSD","BBLEYS","CARFAX","CHURCH","COWLYM","COWLEY","HHLNOR","HEAD","HINKPK","HOLYWE","IFFLDS","JEROSN","LITTM","LYEVAL","MARST","NORTH","NORBRK","OSCB","OCB","QUARIS","RHIFF","STCLEM","STMARG","STMARY","SUMMTN","WOLVER"]

## tabletypes = ["summary", "details", "dates", "constraints", "documents"]

# issue with activeTab=contacts
# the name of the agent doesn't come in a table row.  Will need different handling
# <div class="agents"> <h3>Agent</h3> <p>Mr Robin Akers</p>

def search(wdcode):
    request_data = {
        "searchCriteria.ward": wdcode,
        "date(applicationValidatedStart)": "2017-01-01",
        "date(applicationValidatedEnd)": "2017-12-31"
    }
# is this the way to pass values when posting to a form? A dictionary object with the keys being the names of the controls?
    
    print "POST 'http://public.oxford.gov.uk/online-applications/advancedSearchResults.do?action=firstPage'"
    sleep(2)
    result = requests.post('http://public.oxford.gov.uk/online-applications/advancedSearchResults.do?action=firstPage', request_data)

    result_dom = fromstring(result.content)
	
#  a href="/online-applications/pagedSearchResults.do?action=page&amp;searchCriteria.page=3" = and so on until no more
#  http://public.oxford.gov.uk/online-applications/pagedSearchResults.do?action=page&searchCriteria.page=1
#  test for existence of anchor element with class = "next"?
#  <a href="/online-applications/pagedSearchResults.do?action=page&amp;searchCriteria.page=2" class="next">

    applications = result_dom.xpath("//li[@class='searchresult']")
	
    if len(applications) == 0:
        return
    else:
        for index, application in enumerate(applications):
	    application_link = application.xpath("//a/@href")
	    matchObj = re.search( r'keyVal=(.*$)', application_link)
	    key = matchObj.group(1)

##          for tabletype in tabletypes:
#	    application_url = "http://public.oxford.gov.uk/online-applications/applicationDetails.do?activeTab=summary&keyVal=" + key

            application_url = "http://public.oxford.gov.uk" + application_link
            print "GET " + application_url
            sleep(2)
            application_page = requests.get(application_url)
            application_dom = fromstring(application_page.content)            
            application_table = application_dom.xpath("//table")[0]
			
            for row in application_table.xpath('.//tr'):
                row_heading = "".join(row.xpath('.//th/text()')).strip()
                row_value = "".join(row.xpath('.//td/text()')).strip()
# this doesn't work for all tabs, e.g. activeTab=constraints
                if row_heading == "Reference":
                    reference = row_value
                if row_heading == "Proposal":
                    proposal = row_value
                if row_heading == "Address":
                    address = row_value
                                                
                data = {"ward": wdcode, "reference": reference, "proposal": proposal, "address": address, "index": index}
            
                print data
                scraperwiki.sqlite.save(unique_keys=['reference', 'index'], data=data)
