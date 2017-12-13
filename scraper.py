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
	
	councillor = councillors[2]
	
#	print councillor.strip()
	
	cols = councillor.xpath("td")
	print len(cols)
	
	paras = cols[1].xpath('p')
	
	for i, para in enumerate(paras):
		if i == 0:
			name = "".join(para.xpath('./a/text()')).strip()
			link = "".join(para.xpath('./a/@href')).strip()
		else:
			pText = "".join(para.xpath('text()')).strip()
			print i, pText
			
			if len(para.xpath('a')) ==1:
				link1 = "".join(para.xpath('./a/@href')).strip()
				matchObj = re.search( r'@', link1)
				if matchObj:
					matchObj1 = re.search( r'work', pText, re.I)
					if matchObj1:
						eWork = link1
					else:
						matchObj1 = re.search( r'home', pText, re.I)
						if matchObj1:
							eHome = link1
						else:
							print i, pText, link1
				else:
					print "non email address link"
			else:
				matchObj = re.search( r'OX\d \d[A-Z]{2}', pText)
				if matchObj:
					address = pText
				else:
					matchObj = re.search( r'^(.+)?\:\s+(0[0-9 ]+)$', pText)
					if matchObj:
						number = matchObj.group(2)
						numberType = matchObj.group(1)
						
						if re.search( r'home\s+mob', numberType, re.I):
							homeMobile = number
						elif re.search( r'work\s+mob', numberType, re.I):
							workMobile = number							
						elif re.search( r'home', numberType, re.I):
							homePhone = number							
						elif re.search( r'work', numberType, re.I):
							workPhone = number
					else:
						print i, pText
						roles = roles.join(pText)
						
	
	party = "".join(cols[2].xpath('text()')).strip()
	ward = "".join(cols[3].xpath('text()')).strip()
	
	data = {"name": name, "link": link, "address": address, "roles": roles, "eWork": eWork, "eHome": eHome, "homePhone": homePhone,  "workhone": workhone,  "homeMobile": homeMobile,  "workMobile": workMobile,  "party": party, "ward": ward}
	
	print data
	

	
#	if len(councillors) == 0:
#		return
#	else:
#		for index, councillor in enumerate(councillors):
#			col1 = councillor.xpath(".//td)[1]").strip()
#			data = {"col1": col1, "index": index}
			
#			print data
#			scraperwiki.sqlite.save(unique_keys=['index'], data=data)
		

search()
