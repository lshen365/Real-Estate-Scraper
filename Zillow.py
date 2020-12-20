from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
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

    def read_file(self,zipcode):
        f = open("zipcodes.txt")
        for x in f:
            #TODO Fill in Regex
            file_zip = re.match("")
            if file_zip == zipcode:
                #TODO extract ID from text file
                ID = ""
                return ID
        return False

    def create_link(self, ID):
        #Fill in ID
        url = "" + ID
        return url

    def parse_json(self):
        print("Found the json api")

    def append_to_file(self):
        f = open("zipcodes.txt","a")
        #TODO Append to the end of the file

    def locate_id(self,zipcode):
        #TODO Go onto zillow and find the unique id for the zipcode
        url = "" + zipcode





zipcode = input("What zipcode do you want to look up?: ")
test = Property_Grab()

