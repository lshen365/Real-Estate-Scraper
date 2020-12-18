from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import random
class Property_Grab:
    def __init__(self,):
        # self.set_up_proxy()
        self.driver = webdriver.Chrome()
        opt = Options()
        ua = UserAgent()
        userAgent = ua.random
        self.set_viewport_size(800,600)
        opt.add_argument(f"user-agent={userAgent}")
        opt.add_argument('--disable-blink-features=AutomationControlled')
        self.properties = []
    def delay_in_millisec(self):
        sleep(0.25)
    # def set_up_proxy(self):
    #     req_proxy = RequestProxy()
    #     proxies = req_proxy.get_proxy_list()
    #     us_proxies = []
    #     for x in proxies:
    #         if x.country == "United States":
    #             us_proxies.append(x)
    #     PROXY = us_proxies[0].get_address()
    #     webdriver.DesiredCapabilities.CHROME['proxy']={
    #         "httpProxy":PROXY,
    #         "ftpProxy":PROXY,
    #         "sslProxy":PROXY,
    #
    #         "proxyType":"MANUAL",
    #     }

    def set_viewport_size(self,width, height):
        window_size = self.driver.execute_script("""
            return [window.outerWidth - window.innerWidth + arguments[0],
              window.outerHeight - window.innerHeight + arguments[1]];
            """, width, height)
        self.driver.set_window_size(*window_size)

    def scroll_to_bottom(self):
        for x in range(0,random.randrange(80,100)):
            self.driver.execute_script("window.scrollBy(0, {});".format(x))

    def create_search_query(self,zipcode,page=None):
        if page is not None:
            query = str(zipcode)+"/"+str(page)+"_p"
            print(query)
            return query
        else:
            return zipcode
    def identify_next_page(self):
        def is_disabled():
            try:
                self.driver.find_element_by_xpath("//a[@rel='next' and @tabindex='-1']")
                return True #Found the last page
            except:
                return False

        try:
            if (self.driver.find_element_by_xpath("//a[@rel='next']")):
                if is_disabled():
                    return False
                return True

        except:
            print("Could not find next page button")
            return False

    def search_zillow(self,search_terms):
        try:
            self.driver.get("https://www.zillow.com/homes/"+search_terms)
            # self.driver.find_element_by_xpath("//input[@type='text']").send_keys(search_terms)
            # self.driver.find_element_by_xpath("//button[@id='search-icon']").click()
            page_source = self.driver.page_source
            self.soup = BeautifulSoup(page_source,'lxml')
            return True
        except NoSuchElementException:
            print("Error has occured in search_zillow ")
            return False

    def get_built_status(self,html):
        # Returns: True if house is built
        try:
            footer = html.find_all(class_="list-card-type",limit=1)
            if footer[0].get_text() == "House for sale":
                return True
            else:
                return False
        except:
            print("Built status not found")
            return False

    def get_address(self, html):
        try:
            address = html.find("address").get_text()
            built_status = self.get_built_status(html)
            if built_status:
                #print(address)
                return address
            else:
                return False
        except:
            print("Failed to find address")
            return False

    def get_price_bedroom(self,html):
        try:
            list_card_heading = html.find_all(class_="list-card-heading")[0]
            price = list_card_heading.find("div").get_text()
            list_card_details = list_card_heading.find_all("li")
            bedroom = list_card_details[0].get_text()
            bathroom = list_card_details[1].get_text()
            squareft = list_card_details[2].get_text()
            return price,bedroom,bathroom,squareft
        except:
            return False

    def findProperties(self):

        try:
            zillow_listing_grid = self.soup.find_all(class_="list-card-info")
            for x in zillow_listing_grid:
                address = self.get_address(x)
                if address != False:
                    price,bedroom,bathroom,square_feet = self.get_price_bedroom(x)
                    self.properties.append((price,bedroom,bathroom,square_feet))
                    print(type(self.properties))
                    print("Address: {}, Bedroom: {}, Bathroom: {}, SqrFt: {} ".format(address,price,bedroom,square_feet))
                    print("-----------------------------")

        except NoSuchElementException:
            print("Error has occured in finding zillow_listing_grid or properties value")
    def get_property_list(self):
        return self.properties

    def scan_zillow(self,zipcode):
        if self.search_zillow(zipcode):
            page_tracker = 2
            while self.identify_next_page():
                sleep(5)
                self.findProperties()
                query = self.create_search_query(zipcode,page_tracker)
                page_tracker += 1
                self.scroll_to_bottom()
                sleep(5)
                self.search_zillow(query)



    def close_driver(self):
        self.driver.close()








zipcode = input("What zipcode do you want to look up?: ")
test = Property_Grab()

test.scan_zillow(zipcode)
properties = test.get_property_list()
# test.close_driver()
print(properties)
#test.close_driver()
