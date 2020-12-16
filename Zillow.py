from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

class Zillow:
    def __init__(self):
        self.driver = webdriver.Chrome()
        opt = Options()
        opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        url = 'https://www.zillow.com/homes/80016/'
        self.driver.get(url)
        page_source = self.driver.page_source
        self.soup = BeautifulSoup(page_source,'lxml')

    def get_built_status(self,html):
        # Returns: True if house is built
        try:
            footer = html.find_element_by_class_name("list-card-footer").find_element_by_class_name("list-card-type").text
            if footer == "New construction":
                return False
            else:
                return True
        except:
            return False

    def get_address(self,html):
        try:
            address = html.find_element_by_tag_name("a").find_element_by_tag_name("address")
            built_status = self.get_built_status(html)
            if built_status:
                return address
            else:
                return False
        except:
            print("Failed to find address")
            return False

    # def get_bedroom_information:

    def findProperties(self):

        try:
            zillow_listing_grid = self.soup.find_all(class_="list-card-info")
            for x in zillow_listing_grid:
                property_information = self.get_propertyInformation(x)
                if property_information:
                    address = self.get_address(property_information)

        except:
            print("Error has occured in finding zillow_listing_grid or properties value")






test = Zillow()
test.findProperties()
