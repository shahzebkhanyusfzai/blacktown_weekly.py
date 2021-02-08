import scrapy
from selenium import webdriver
from scrapy import Selector
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
ua = UserAgent()
import os 
import requests
from collections import OrderedDict
from datetime import date
from selenium.webdriver.common.keys import Keys



class blacktown_weekly(scrapy.Spider):
    name = 'blacktownweekly'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.google.com']
    ua = UserAgent()

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'monthly_data.csv',
        'FEED_EXPORT_ENCODING':'utf-8'
    }
    
    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument("start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--incognito')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--use-fake-ui-for-media-stream")
        self.options.add_argument(
            f'--user-agent={self.ua.chrome}')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=self.options)


    def parse(self,response):
        self.driver.get("https://eservices.blacktown.nsw.gov.au/T1PRProd/WebApps/eProperty/P1/eTrack/eTrackApplicationSearchResults.aspx?Field=S&Period=LW&r=BCC.P1.WEBGUEST&f=%24P1.ETR.SEARCH.SLW&ApplicationId=CC-21-00049")
        self.driver.implicitly_wait(10) 

        l=[]
        q=1
        v=1

        while True:
            
            resp = Selector(text=self.driver.page_source) 
            page_nos = resp.xpath('((//tbody)[2]/tr/td)/a/text()').getall()
            
            
            v=v+1
            print(v)

            time.sleep(1)    
            
            links = resp.xpath('(//a)[position()>32 and position()<62 ][position() mod 2 = 1]/text()').getall()
            
            # Getting all the links of DA20/xx
            for a in links: 
                
                
                a = a.strip()
                if a in ['...']:
                    break
                elif a in ['1']:
                    break
                else:
                    a = 'https://eservices.blacktown.nsw.gov.au/T1PRProd/WebApps/eProperty/P1/eTrack/eTrackApplicationDetails.aspx?r=BCC.P1.WEBGUEST&f=%24P1.ETR.APPDET.VIW&ApplicationId='+a
                    l.append(a)
           
    # from line 72 to line 90 we are dealing with first 11 pages                    
                        
            time.sleep(3)
           
    # ///////////////////////////// FIRST type ///////////////////////
            if a in ['...']:
                print('////////print break exe////////')
                break
            elif a in ['1']:
                break    
            elif len(l)<= 165:
                
                if q <11:
                    q = q+1
                    self.driver.find_element_by_xpath('((//tbody)[2]/tr/td)[position()='+str(int(q))+']').click() 
                    time.sleep(2)
        
                elif q==11:
                    time.sleep(2)
                    q = 3
                    self.driver.find_element_by_xpath('((//tbody)[2]/tr/td)[position()='+str(int(q))+']').click()
                    time.sleep(2)
                    q=q+1
                    time.sleep(2)

# ///////////////////////// second type ////////////////////////////////
                
            elif len(l)>165:

                if len(page_nos)==11 and page_nos[-1] in ['...'] and page_nos[-11] in ['...']:


                    if q==12:
                        nextnumber = int(str(page_nos[-2]))
                        time.sleep(2)
                        self.driver.find_element_by_xpath('((//tbody)[2]/tr/td)[position()='+str(int(q))+']').click()
                        time.sleep(2)
                        q=q+1
                        page_2_again = 1
                        

                    elif q <12:
                        time.sleep(2)
                        self.driver.find_element_by_xpath('((//tbody)[2]/tr/td)[position()='+str(int(q))+']').click()
                        time.sleep(2)
                        q = q+1
                        
                        
                    
                    elif page_2_again ==1 and q == 13:
                        q=3 
                        time.sleep(3)
                        self.driver.find_element_by_xpath('((//tbody)[2]/tr/td)[position()='+str(int(q))+']').click()
                        q = q+1
                        time.sleep(2)



            

    # /////////////////// third type ///////////////////////////////////                    

                elif len(page_nos) < 11 and page_nos[-10] in ['...']:
                    if q<12:
                        time.sleep(2)
                        self.driver.find_element_by_xpath('((//tbody)[2]/tr/td)[position()='+str(int(q))+']').click()
                        time.sleep(2)
                        q= q+1
                        time.sleep(2)

                    elif q==13:
                        time.sleep(15)
                        q=int(14)+nextnumber-int(str(page_nos[-1]))
                        self.driver.find_element_by_xpath('((//tbody)[2]/tr/td)[position()='+str(int(q))+']').click()
                        time.sleep(2)
                        q=q+1
                        
                

        for link in l:
           
            self.driver.get(link)
        
            time.sleep(2)
            resp1 = Selector(text=self.driver.page_source)
            application_ID = resp1.xpath('(((//tbody)[1]/tr[@class="normalRow"])[1]/td)[2]/text()').get()
            description = resp1.xpath ('(((//tbody)[1]/tr[@class="alternateRow"])[1]/td)[2]/text()').get().replace('â€“','')
            Group = resp1.xpath('(((//tbody)[1]/tr[@class="normalRow"])[2]/td)[2]/text()').get()
            Category = resp1.xpath('(((//tbody)[1]/tr[@class="alternateRow"])[2]/td)[2]/text()').get()
            Sub_category = resp1.xpath('(((//tbody)[1]/tr[@class="normalRow"])[3]/td)[2]/text()').get().strip().replace('â€“','')
            status = resp1.xpath('(((//tbody)[1]/tr[@class="alternateRow"])[3]/td)[2]/text()').get()
            Lodgement_Date = resp1.xpath('(((//tbody)[1]/tr[@class="normalRow"])[4]/td)[2]/text()').get()
            stage_decision = resp1.xpath('(((//tbody)[1]/tr[@class="alternateRow"])[4]/td)[2]/text()').get().strip()
            Estimated_cost = resp1.xpath ('(((//tbody)[1]/tr[@class="normalRow"])[5]/td)[2]/text()').get()
            Name = resp1.xpath('((//tbody)[2]/tr[@class="normalRow"]/td)[2]/text()').get()
            Association = resp1.xpath ('((//tbody)[2]/tr[@class="alternateRow"]/td)[2]/text()').get()
            
            yield {

                'Application ID': application_ID,
                'Description': description,
                'Group': Group,
                'Category': Category,
                'Sub-Category': Sub_category,
                'status' : status,
                'Lodgement date ': Lodgement_Date,
                'Stage/Decision' : stage_decision,
                'Estimated cost':Estimated_cost,
                'Name':Name,
                'Association': Association,
            
            }
            
process = CrawlerProcess()
process.crawl(blacktown_weekly)
process.start()
driver.quit()







