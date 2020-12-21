from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import random
import requests
import json
from urllib.request import urlopen
class Property_Grab:
    def __init__(self,):
        # self.set_up_proxy()
        self.zipcodes = {}

    def read_file(self,zipcode):
        f = open("zipcodes.txt")
        count = 1 # Skips the first line
        for x in f:
            if count != 1:
                file_zip = x.split()
                if file_zip[0] == zipcode:
                    self.ID = file_zip[1]
                    print(self.ID)
                    f.close()
                    return True
            else:
                count += 1
        print("Zipcode not found")
        f.close()
        return False

    def zipcodes_append(self, key, value):
        self.zipcodes[key] = value

    def zipcodes_get(self, key):
        return self.zipcodes[key]

    def create_link(self):
        url = "https://www.zillow.com/homes/" + self.ID
        return url

    def parse_json(self):
        print("Found the json api")

    def append_to_file(self):
        f = open("zipcodes.txt","a")
        #TODO Append to the end of the file

    def locate_id(self,zipcode):
        #TODO Go onto zillow and find the unique id for the zipcode
        url = "https://www.zillow.com/homes/" + zipcode+"_rb"
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                   'Accept-Encoding': 'identity'
                   }
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.content,'lxml')
        data = str(soup.find('script',{"data-zrr-shared-data-key":"mobileSearchPageStore"}))
        data = data.replace("\"","")
        #data = data.replace("<","")
       # data = data.replace("{","")
        #data = data.replace("}","")
        #data = data.replace("[","")
        #data = data.replace("]","")
        #data = data.replace(":"," ")

        for x in data.split(","):
            print(x)
            if(re.match("mapBounds",x) != None):
                print(x)
                print(re.search("mapBounds",x).group(0))






zipcode = input("What zipcode do you want to look up?: ")
test = Property_Grab()
test.locate_id(zipcode)


