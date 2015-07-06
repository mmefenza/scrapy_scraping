#######################################################################################################################################
# Author : Michael Mefenza Nentedem
# Task: scrap data from dynamic websites and output a JSON file
# Output: JSON file
# Output Fields
#    name : company's name
#
#    desc : company's description
#
#    loc : company's location
#
#    services : company'sservices
#
#    joined : company's joined
#
#    followers : company's number of followers
#
#    link : company's webpage on xxx
#
#    full_desc : company's full description
#
#    product :  company's product
#
#    q_and_a :  company's questions and answers
#
#    founders :  company's founders. 
#		 Format in JSON file : Founder_1_data + " #&#& " + Founder_2_data + " #&#& " + ... + " #&#& " + Founder_n_data 
#		 where n is the number of funders
#                Founder_i_data = founder_name + " #& " + founder_desc + " #& " + infos_data + " #& " + references + " #& " + yyy_data
#                yyy_data  = yyy_name+ " && " + yyy_desc + " && " + yyy_current + " && " + yyy_education + " && " + #			                  yyy_experiences + " && " + yyy_educations
#       
#    incubators : company's incubators
#		  Format in JSON file : incubator_1 + " && " + incubator_2+ " && " + ... + " && " + incubator_n
#		  where n is the number of incubators
#
#    portfolio : company's portfolio
#		 Format in JSON file : portfolio_1_data + " && " + portfolio_2_data + " && " + ... + " && " + portfolior_n_data
#		 where n is the number of elements in the portfolio
#                portfolio_i_data = category's portfolio + " : " + value inside categorie
#		 examples of category's portfolio: Acquired, Customer, ...
#
#    team :   company's team
#		 Format in JSON file : team_1_data + " # " + team_2_data + " # " + ... + " # " + team_n_data
#		 where n is the number of elements in the team
#                team_i_data = category's team + " : " + values inside categorie
#                values inside categorie = value_1 + " && " + value_2 + " && " + ... + " && " + value_m
#		 where m is the number of elements in the category
#		 examples of category's team: Employees , Past Employees , Board Members, ...
#
#    activity_tab : company's activity
#		  Format in JSON file : activity_1 + " && " + activity_2+ " && " + ... + " && " + activity_n
#		  where n is the number of activities
#
#    fundings :  company's fundings
#		 Format in JSON file : funding_1_data + " #&#& " + funding_2_data + " #&#& " + ... + " #&#& " + funding_n_data 
#		 where n is the number of fundings
#                funding_i_data = serie + " : " + date_serie + " : " + amount_serie + " : " + valuation_serie  + " : " + participants 
#                participants = participant_1_data + " &&& " + participant_2_data + " &&& " + ... + " &&& " + participant_m_data  
#		 participant_i_data = name + " :: " + desc
#
#    twts : company's twts
#		 Format in JSON file : nb_twts + " : " + nb_following + " : " + nb_followers + " : " + list_of_twts
#                list_of_twts = value_1 + " && " + value_2 + " && " + ... + " && " + value_m
#		 where m is the number of twts. m <=200
#                 
#    investors : company's investors
#		 Format in JSON file : investor_1_data + " #&#& " + investor_2_data + " #&#& " + ... + " #&#& " + investor_n_data 
#		 where n is the number of investors
#                investor_i_data = investor_name + " #& " + investor_desc + " #& " + infos_data + " #& " + references
#
#    followers_info : company's followers
#		 Format in JSON file : follower_1_data + " #&#& " + follower_2_data + " #&#& " + ... + " #&#& " + follower_n_data 
#		 where n is the number of followers
#                follower_i_data = followers_name + " #& " + followers_desc + " #& " + followers_confirmed_investments+ " #& " + #		                   followers_location+ " #& " +followers_education+ " #& " +infos_data + " #& " + references 
#######################################################################################################################################
import scrapy
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from bigdata.items import BigdataItem
import time

class BigdataSpider(scrapy.Spider):
	name = "bigdata"
	allowed_domains = ["xxx.com","zzz.com", "yyy.com"]
	start_urls = [
	"https://xxx/url"
	]
	def __init__(self):
		self.driver = webdriver.Firefox()
                self.driver1 = webdriver.Firefox()
                self.driver2 = webdriver.Firefox()
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def parse(self, response):
		self.driver.get(response.url)
		self.driver.implicitly_wait(1)  
                ####click on more to display all companies
		more_button = self.driver.find_element_by_xpath('//div[@class="more hidden"]')
		for i in range(25):
			 more_button.click()
			 self.driver.implicitly_wait(1)
			 time.sleep(1) 
                ####container for all companies
		next = self.driver.find_elements_by_xpath('//div[@class="base item"]')
                ####process companies, one by one
		for a in next:
			item = BigdataItem()
			try:    
                                ####retrieve company data on fist page
				item['name'] = a.find_element_by_xpath('.//div[@class="name"]//a').text
				self.logger.info('Item name being processed %s', item['name'])
				#if item['name'] == "Return Path" :
				try: 
					item['desc'] = a.find_element_by_xpath('.//div[@class="blurb"]').text
				except:
					item['desc'] =''
				try: 
					item['loc'] = a.find_element_by_xpath('.//div[@class="tags"]//a[1]').text
				except:
					item['loc'] =''
				try: 
					item['services'] = a.find_element_by_xpath('.//div[@class="tags"]//a[2]').text
				except:
					item['services'] =''
				try: 
					item['joined'] = a.find_element_by_xpath('.//div[@class="column joined"]//div[@class="value"]').text
				except:
					item['joined'] =''
				try: 
					item['followers'] = a.find_element_by_xpath('.//div[@class="column followers"]//div[@class="value"]').text
				except:
					item['followers'] =''
				try: 
					item['link'] = a.find_element_by_xpath('.//div[@class="name"]//a').get_attribute("href")
				except:
					item['link'] =''
                                ####go to company page
				yield Request(url=item['link'], meta={'item': item},callback=self.parse_companylink)
			except:
				item['name'] ='' 

    
	def parse_companylink(self,response):
                ####process company page data
		item = response.meta['item']
		i = 0
		self.driver1.implicitly_wait(2)  
		self.driver1.get(response.url)
		try:    
			item['full_desc'] = self.driver1.find_element_by_xpath('//div[@class="tags"]').text
		except:
			item['full_desc'] =''
		try: 
			item['product'] = self.driver1.find_element_by_xpath('//div[@class="product_desc editable_region"]').text
		except:
			item['product'] =''		
		try: 
			i=0
			incubator = self.driver1.find_elements_by_xpath('//div[@data-role="incubator"]//ul[@class="medium roles"]//li[@class="role"]')
			for b in incubator:
				if i==0 :
					item['incubators']= b.text
					i=1
				else: 
					item['incubators']= item['incubators']+ " && " + b.text  
		except:
			item['incubators'] =''   
		try: 
			i=0
			portfolios= self.driver1.find_elements_by_xpath('//div[@class="two_col_block"]//div[not(contains(@class,"hidden")) and not(contains(@class,"left_block")) and not(contains(@class,"right_block"))]')
			for b in portfolios:
				if i==0 :
					item['portfolio']= b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text
					i=1
				else: 
					item['portfolio']= item['portfolio']+ " && " + b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text 
		except:
			item['portfolio'] =''  
		try: 
			item['q_and_a'] = self.driver1.find_element_by_xpath('//div[@class="qa section"]').text
		except:
			item['q_and_a'] =''
                ####click on view all buttons
                try:
			view_all_buttons = self.driver1.find_elements_by_xpath('//a[@class="view_all"]')
			for b in view_all_buttons:
				b.click()
				self.driver1.implicitly_wait(1)
				time.sleep(1)
                except:
			time.sleep(1)
                ####retrieve team	
		try: 
			i=0
			teams= self.driver1.find_elements_by_xpath('//div[@class="section team"]//div[@class="group"]')
			for b in teams:
                                datarole = b.find_element_by_xpath('.//div[contains(@class," dsr31 startup_roles fsp87")]').get_attribute("data-role")
				members =  b.find_elements_by_xpath('.//div[@class="g-lockup top medium"]')
				if i==0 :
					item['team']= datarole + " : "
                                        j=0
					for c in members:
                                                if j==0 :
							item['team']= item['team'] + c.text
							j=1
						else:
							item['team']= item['team'] +" && "+ c.text
					i=1
				else: 
					item['team']= item['team'] + " # " + datarole + " : "
                                        j=0
					for c in members:
                                                if j==0 :
							item['team']= item['team'] + c.text
							j=1
						else:
							item['team']= item['team'] +" && "+ c.text
		except:
			item['team'] ='' 
                ####retrieve founders	
                item['founders'] ='' 
                try:    	
			founder = self.driver1.find_elements_by_xpath('//div[@class="founders section"]//div[@class="g-lockup top larger"]')
			for b in founder:
				founder_link =  b.find_element_by_xpath('.//div[@class="name"]//a').get_attribute("href")
				self.driver2.implicitly_wait(2)  
				self.driver2.get(founder_link)
				try:
					founder_name = self.driver2.find_element_by_xpath('//div[@class="summary"]//h1[@class="name"]').text
				except:
					founder_name=''
				try:                                
					founder_desc = self.driver2.find_element_by_xpath('//div[@class="summary"]//div[@data-field="bio"]').text
				except:
					founder_desc=''

				infos_data =''
				infos= self.driver2.find_elements_by_xpath('//div[contains(@class,"two_col_block")]//div[not(contains(@class,"hidden")) and not(contains(@class,"left_block")) and not(contains(@class,"right_block"))]')
				i = 0
				for b in infos:
					if i==0 :
						infos_data = b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text
						i=1
					else: 
						infos_data = infos_data + " && " + b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text 
				try:
					reviews= self.driver2.find_elements_by_xpath('//ul[contains(@class,"reviews")]//li[contains(@class,"review")]')
				except:
					reviews= self.driver2.find_elements_by_xpath('//ul[contains(@class,"reviews")]')
				references =''
				i = 0
				for c in reviews:
					if i==0 :
						references= c.text
						i=1
					else: 
						references= references+ " && " + c.text   
				yyy_data=''
				try:
					yyy_link = self.driver2.find_element_by_xpath('//div[@class="actions_container"]//a[contains(@data-field,"yyy_url")]')
				except:
					yyy_link=''
				if yyy_link!='' :
					self.driver2.execute_script("arguments[0].setAttribute('target', '_parent')",yyy_link);
					yyy_link.click()
					self.driver2.implicitly_wait(1)  
					time.sleep(1)
					yyy_name = self.driver2.find_element_by_xpath('//div[@id="name"]').text
					yyy_desc = self.driver2.find_element_by_xpath('//div[@id="headline"]').text
				        try:
						yyy_current = self.driver2.find_element_by_xpath('//tr[@id="overview-summary-current"]//ol').text
						yyy_education = self.driver2.find_element_by_xpath('//tr[@id="overview-summary-education"]//ol').text
						lexperiences = self.driver2.find_elements_by_xpath('//div[@id="background-experience"]//div[contains(@id,"experience") and contains(@id,"view")]')
						i=0
						yyy_experiences=''
						for c in lexperiences:
							if i==0:
								i=1
								role = c.find_element_by_xpath('//h4').text
								place = c.find_element_by_xpath('//h5').text
								duration = c.find_element_by_xpath('//span[@class="experience-date-locale"]').text
								yyy_experiences = role + " __ " + place + " __ " + duration
							else:
								role = c.find_element_by_xpath('//h4').text
								place = c.find_element_by_xpath('//h5').text
								duration = c.find_element_by_xpath('//span[@class="experience-date-locale"]').text
								yyy_experiences = yyy_experiences + " #__# " + role + " __ " + place + " __ " + duration
						leducations = self.driver2.find_elements_by_xpath('//div[@id="background-education"]//div[contains(@id,"education") and contains(@id,"view")]')
						i=0
						yyy_educations=''
						for c in leducations:
							if i==0:
								i=1
								school = c.find_element_by_xpath('//h4').text
								major = c.find_element_by_xpath('//h5').text
								year = c.find_element_by_xpath('//span[@class="education-date"]').text
								yyy_educations = school + " __ " + major + " __ " + year
							else:
								role = c.find_element_by_xpath('//h4').text
								place = c.find_element_by_xpath('//h5').text
								duration = c.find_element_by_xpath('//span[@class="education-date"]').text
								yyy_educations = yyy_educations + " #__# " + school + " __ " + major + " __ " + year
						yyy_data = yyy_name+ " && " + yyy_desc + " && " + yyy_current + " && " + yyy_education + " && " + yyy_experiences + " && " + yyy_educations
					except:
						yyy_data = yyy_name+ " && " + yyy_desc
				item['founders']= item['founders']+ " #&#& " + founder_name + " #& " + founder_desc + " #& " + infos_data + " #& " + references + " #& " + yyy_data       
                except:
			item['founders'] ='' 
		####retrieve investors	
		item['investors'] ='' 
		try: 
			investors= self.driver1.find_elements_by_xpath('//div[contains(@class,"past_financing")]//div[@data-role="past_investor"]//li[@class="role"]')
			for b in investors:                                
				investor_link =  b.find_element_by_xpath('.//div[@class="name"]//a').get_attribute("href")
		                self.driver2.implicitly_wait(2)  
				self.driver2.get(investor_link)
				try:                                
					investor_name = self.driver2.find_element_by_xpath('//div[@class="summary"]//h1[@class="name"]').text
				except:
					investor_name=''

				try:                                
					investor_desc = self.driver2.find_element_by_xpath('//div[@class="summary"]//div[@data-field="bio"]').text
				except:
					investor_desc=''

				infos_data =''
				try:
					infos= self.driver2.find_elements_by_xpath('//div[contains(@class,"two_col_block")]//div[not(contains(@class,"hidden")) and not(contains(@class,"left_block")) and not(contains(@class,"right_block"))]')
				except:
					infos=''
				i = 0
				for b in infos:
					if i==0 :
						infos_data = b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text
						i=1
					else: 
						infos_data = infos_data + " && " + b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text 
				try:
					reviews= self.driver2.find_elements_by_xpath('//ul[contains(@class,"reviews")]//li[contains(@class,"review")]')
				except:
					reviews= self.driver2.find_elements_by_xpath('//ul[contains(@class,"reviews")]')
				references =''
				i = 0
				for c in reviews:
					if i==0 :
						references= c.text
						i=1
					else: 
						references= references+ " && " + c.text   
				item['investors']= item['investors']+ " #&#& " + investor_name + " #& " + investor_desc + " #& " + infos_data + " #& " + references           
                except:
			item['investors'] ='' 
		####retrieve fundings 
                try:
			view_all_buttons_fundings = self.driver1.find_elements_by_xpath('//a[@class="more_participants_link"]')
			for b in view_all_buttons_fundings:
				b.click()
				self.driver1.implicitly_wait(1)
				time.sleep(1)
                except:
			time.sleep(1)
		try: 
			i =0
			funding = self.driver1.find_elements_by_xpath('//div[contains(@class,"past_financing")]//li[contains(@class,"startup_round")]')
			for b in funding :
				serie = b.find_element_by_xpath('.//div[contains(@class,"type")]').text
				date_serie = b.find_element_by_xpath('.//div[contains(@class,"date_display")]').text
				amount_serie = b.find_element_by_xpath('.//div[contains(@class,"raised")]').text
		                try: 
					valuation_serie = b.find_element_by_xpath('.//div[contains(@class,"valuation")]').text
				except:
					valuation_serie=''
		                participants = b.find_elements_by_xpath('.//div[contains(@class,"participant ")]')
				j =0
		                participant =''
				for c in participants:
		                        if j==0 :
						participant = c.find_element_by_xpath('.//div[contains(@class,"name")]').text + " :: " + c.find_element_by_xpath('.//div[contains(@class,"tags")]').text
						j=1
					else:
						participant = participant +" &&& "+ c.find_element_by_xpath('.//div[contains(@class,"name")]').text + " :: " + c.find_element_by_xpath('.//div[contains(@class,"tags")]').text
				if i==0 :
					item['fundings']= serie + " : " + date_serie + " : " + amount_serie + " : " + valuation_serie  + " : " + participant
					i =1
				else: 
					item['fundings']= item['fundings']+ " && " + serie + " : " + date_serie + " : " + amount_serie + " : " + valuation_serie  + " : " + participant 
		except:
			item['fundings'] ='' 
                ####navigate to activities
		try: 
			activity_tab_link = self.driver1.find_element_by_xpath('//a[@data-name="activity"]')
			activity_tab_link.click()
			self.driver1.implicitly_wait(1)
			time.sleep(1)
                except:
			time.sleep(1)
                i=0
                while True:
                	try:
				activity_tab_link_more = self.driver1.find_element_by_xpath('//a[contains(@class,"g-feed_more") and not(contains(@class,"disabled"))]')
				activity_tab_link_more.click()
				self.driver1.implicitly_wait(1)
				time.sleep(1)
                                i = i+1
                                if i==30:
					break
                        except:
				break
		try: 
			i=0
			activities= self.driver1.find_elements_by_xpath('//div[@class="updates"]//div[contains(@class,"dssh0")]')    
			for b in activities:
				if i==0 :
					item['activity_tab']= b.text
					i=1
				else: 
					item['activity_tab']= item['activity_tab']+ " && " + b.text  
		except:
			item['activity_tab'] =''
                ####navigate to followers
		try:
			follower_tab_link = self.driver1.find_element_by_xpath('//a[@data-name="followers"]')
			follower_tab_link.click()
			self.driver1.implicitly_wait(1)
			time.sleep(1)
                except:
			time.sleep(1)
                ##more button on follower tab is not working
                #i=0
                #while True:
                #	try:
		#		follower_tab_link_more = self.driver1.find_element_by_xpath('//a[contains(@class,"g-feed_more") and not(contains(@class,"disabled"))]')
		#		follower_tab_link_more.click()
		#		self.driver1.implicitly_wait(1)
		#		time.sleep(1)
                #               i = i+1
                #               if i==30:
		#			break
                #        except:
		#		break   
                item['followers_info'] =''
                try:   	
			followers = self.driver1.find_elements_by_xpath('//div[@class="entity"]')
			for b in followers:
				followers_link =  b.find_element_by_xpath('.//div[@class="name"]//a').get_attribute("href")
				self.driver2.get(followers_link)
				try:
					followers_name = self.driver2.find_element_by_xpath('//div[@class="summary"]//h1[@class="name"]').text
				except:
					followers_name=''
				try:                                
					followers_desc = self.driver2.find_element_by_xpath('//div[@class="summary"]//div[@data-field="bio"]').text
				except:
					followers_desc=''
				try:                                
					followers_confirmed_investments = self.driver2.find_element_by_xpath('//span[contains(@oldtitle,"investments confirmed"]').text
				except:
					followers_confirmed_investments=''
				try:                                
					followers_location = self.driver2.find_element_by_xpath('//span[@itemprop="locality"]').text
				except:
					followers_location=''
				try:                                
					followers_education = self.driver2.find_element_by_xpath('//div[@data-field="tags_colleges"]//div[@data-field="tags_colleges"]').text
				except:
					followers_education=''
				infos_data =''
				try:
					infos= self.driver2.find_elements_by_xpath('//div[contains(@class,"two_col_block")]//div[not(contains(@class,"hidden")) and not(contains(@class,"left_block")) and not(contains(@class,"right_block"))]')
				except:
					infos= ''
				i = 0
				for b in infos:
					if i==0 :
						infos_data = b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text
						i=1
					else: 
						infos_data = infos_data + " && " + b.find_element_by_xpath('.//div[@class="left_block"]').text + " : " + b.find_element_by_xpath('.//div[contains(@class,"right_block")]').text 
				try:
					reviews= self.driver2.find_elements_by_xpath('//ul[contains(@class,"reviews")]//li[contains(@class,"review")]')
				except:
					reviews= self.driver2.find_elements_by_xpath('//ul[contains(@class,"reviews")]')
				references =''
				i = 0
				for c in reviews:
					if i==0 :
						references= c.text
						i=1
					else: 
						references= references+ " && " + c.text   
				item['followers_info']= item['followers_info']+ " #&#& " + followers_name + " #& " + followers_desc + " #& " + followers_confirmed_investments+ " #& " +followers_location+ " #& " +followers_education+ " #& " +infos_data + " #& " + references   
                except:
               		item['followers_info'] ='' 
		####get twts
                try:
			tweeter_link = self.driver1.find_element_by_xpath('//a[contains(@class,"zzz_url")]').get_attribute("href")
		        ####go to company zzz page
			self.driver1.implicitly_wait(2)  
			self.driver1.get(tweeter_link)
			try:
				nb_twts= self.driver1.find_element_by_xpath('//a[@data-nav="twts"]//span[@class="ProfileNav-value"]').text
			except:
				nb_twts=''
			try:
				nb_following= self.driver1.find_element_by_xpath('//a[@data-nav="following"]//span[@class="ProfileNav-value"]').text
			except:
				nb_following=''
			try:
				nb_followers= self.driver1.find_element_by_xpath('//a[@data-nav="followers"]//span[@class="ProfileNav-value"]').text
			except:
				nb_followers=''
		                      
		        item['twts'] = nb_twts + " : " + nb_following + " : " + nb_followers

                        i=0
		        while True:
		        	try:
					tw_link_hasmore = self.driver1.find_element_by_xpath('//div[contains(@class,"has-more-items")]')
		                        ##scroll down
					self.driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(1)
                                        i = i+1
                                        if i==30:
						break
		                except:
					break
			try: 
				i=0
		                j=0
				twts = self.driver1.find_elements_by_xpath('//div[contains(@class,"profile-stream")]//div[@class="content"]') 
				for b in twts:
					if i==0 :
						item['twts']= item['twts']+ " : " + b.text
						i=1
					else: 
						item['twts']= item['twts']+ " && " + b.text
		                        j= j +1
					if j==200 :
						break
		                          
			except:
				item['twts'] = nb_twts + " : " + nb_following + " : " + nb_followers               
                except:
			time.sleep(1)	
		yield item 	

	def spider_closed(self, spider):
		self.driver.close()
		self.driver1.close()
                self.driver2.close()
		

	 
