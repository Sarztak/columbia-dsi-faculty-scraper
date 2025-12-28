# new_selector.xpath("//a[@class='inline-block group']/@href").getall() //get all the links on a page
# new_selector.xpath("//h1[@class='font-bold type-preset-2']/text()").get() //name of the faculty 
# new_selector.xpath("//dl[@class='mt-8']//text()").getall() // department of the faculty
# new_selector.xpath("//div[@class='border-t border-slate-100 text-blue-400']//a/@href").getall() //link to personal page
# new_selector.xpath("//div[@class='gutenberg-editor']/p/text()").getall() // info of the faculty
# new_selector.xpath("//div[@class='pagination text-center']/a/@href").get() // next page
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scrapy import Selector
driver_path = r'.\chromedriver.exe'
brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

service = Service(driver_path)
option = webdriver.ChromeOptions()
option.binary_location = brave_path
browser = webdriver.Chrome(service=service, options=option)
browser.get("https://datascience.columbia.edu/people-type/faculty/")
new_selector = Selector(text=browser.page_source)
with open('DSI Faculty.txt', "w", encoding="utf-8") as w:
    while next_page:=new_selector.xpath("//div[@class='pagination text-center']/a[@class='next page-numbers']/@href").get():
        for faculty in new_selector.xpath("//a[@class='inline-block group']/@href").getall():
            browser.get(faculty)
            info_selector = Selector(text=browser.page_source)
            name = info_selector.xpath("//h1[@class='font-bold type-preset-2']/text()").get() # name of the faculty 
            dept = info_selector.xpath("//dl[@class='mt-8']//text()").getall() # department of the faculty
            links = info_selector.xpath("//div[@class='border-t border-slate-100 text-blue-400']//a/@href").getall() # link to personal page
            info = info_selector.xpath("//div[@class='gutenberg-editor']/p/text()").getall() # info of the faculty
            w.write(f'{name}\n')
            for line in dept:
                w.write(f"{line.strip()}\n")
            for link in links:
                w.write(f'\n{link}')
            w.write('\n\n')
            for i in info:
                w.write(f"{i}")
            w.write('\n\n\n==============================================================================================================================================\n\n\n')
        browser.get(next_page)
        print(next_page)
        new_selector = Selector(text=browser.page_source)
