import re
import scraperwiki
import requests
from lxml.html.soupparser import fromstring
from time import sleep

def search():
	urlBase = "http://mycouncil.oxford.gov.uk/"
	
#	print "GET 'http://mycouncil.oxford.gov.uk/mgMemberIndex.aspx?FN=ALPHA&VW=TABLE&PIC=1'" 
	sleep(2)
	result = requests.get(urlBase + 'mgMemberIndex.aspx?FN=ALPHA&VW=TABLE&PIC=1')
	
	result_dom = fromstring(result.content)
	councillors = result_dom.xpath("//table[@id='mgTable1']//tr")
	
	if len(councillors) == 0:
		return
	else:
		for index, councillor in enumerate(councillors):	

			roles = ""
			eHome = ""
			eWork = ""
			homePhone = ""
			workPhone = ""
			homeMobile = ""
			workMobile = ""
			surgery = ""
			
	#	data = {"name": name, "link": link, "address": address, "roles": roles, "eWork": eWork, "eHome": eHome, "homePhone": homePhone,  
	#                "workhone": workhone,  "homeMobile": homeMobile,  "workMobile": workMobile,  "party": party, "ward": ward}

			cols = councillor.xpath("td")
			if len(cols) == 4:

				paras = cols[1].xpath('p')

				for i, para in enumerate(paras):
					if i == 0:
						name = "".join(para.xpath('./a/text()')).strip()
						link = "".join(para.xpath('./a/@href')).strip()
					else:
						pText = "".join(para.xpath('text()')).strip()
	#					print i, pText

						if len(para.xpath('a')) ==1:
							link1 = "".join(para.xpath('./a/@href')).strip()
							matchObj = re.search( r'@', link1)
							if matchObj:
								matchObj1 = re.search( r'work', pText, re.I)
								if re.search( r'work', pText, re.I):
									eWork = link1
								elif re.search( r'home', pText, re.I):
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
#									print i, pText
									roles = roles.join(pText)


				party = "".join(cols[2].xpath('text()')).strip()
				ward = "".join(cols[3].xpath('text()')).strip()	
				
				sleep(2)
				
#				print "GET " + urlBase + link 
				
				result1 = requests.get(urlBase + link)				
				result_dom1 = fromstring(re.sub(u"(\u2018|\u2019)", "'", result1.content))
				mgUserBody = result_dom1.xpath("//div[@class='mgUserBody']")[0]
				mgUserBodySectionTitles = mgUserBody.xpath("//h2[@class='mgSectionTitle']")
				
				print len(mgUserBodySectionTitles)
				
				for mgUserBodySectionTitle in mgUserBodySectionTitles:
					
					mgUserBodySection = mgUserBodySectionTitle.xpath('following-sibling::*')[0]					
					
					if mgUserBodySection:						
						mgUserBodySectionName = "".join(mgUserBodySectionTitle.xpath('text()')).strip()
						
						matchObj = re.search( r'Surgery details', mgUserBodySectionName, re.I)
						if re.search( r'Surgery details', mgUserBodySectionName, re.I):
							surgery = re.sub(u"(\u2018|\u2019)", "'", "".join(mgUserBodySection.xpath('text()')).strip())							
						elif re.search( r'terms of office', mgUserBodySectionName, re.I):							
							print mgUserBodySectionName, len(mgUserBodySection.xpath('li'))
						elif re.search( r'More information about this councillor', mgUserBodySectionName, re.I):							
							print mgUserBodySectionName, len(mgUserBodySection.xpath('li'))
						elif re.search( r'committee appointments', mgUserBodySectionName, re.I):							
							print mgUserBodySectionName, len(mgUserBodySection.xpath('li'))
						elif re.search( r'Appointments to outside bodies', mgUserBodySectionName, re.I):							
							print mgUserBodySectionName, len(mgUserBodySection.xpath('li'))
						elif re.search( r'Additional Information', mgUserBodySectionName, re.I):							
							print mgUserBodySection.tag
							
					else:
						print "No next sibling"

				
				data = { "index": index, "surgery": surgery, "name": name, "link": link, "address": address, "roles": roles, "eWork": eWork, "eHome": eHome, "homePhone": homePhone,  "workPhone": workPhone,  "homeMobile": homeMobile,  "workMobile": workMobile,  "party": party, "ward": ward}

				scraperwiki.sqlite.save(unique_keys=['index', 'link'], data=data)

#				print data
	


search()
