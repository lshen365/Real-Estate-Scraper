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
    def __init__(self,zip,filters):
        # self.set_up_proxy()
        self.zipcode = zip
        self.zipcode_dict = {}
        self.read_file()
        self.rent, self.fsba, self.fsbo, self.forAuction, self.foresale, self.premarket = filters
        print(self.fsba)
    def read_file(self):
        f = open("zipcodes.txt")
        count = 1 # Skips the first line
        for x in f:
            if count != 1:
                line = x.split()
                zip = line[0]
                self.zipcode_dict[zip] = {}
                self.zipcode_dict[zip]["RegionID"] = line[1]
                self.zipcode_dict[zip]["RegionType"] = line[2]
                self.zipcode_dict[zip]["West"] = line[3]
                self.zipcode_dict[zip]["East"] = line[4]
                self.zipcode_dict[zip]["South"] = line[5]
                self.zipcode_dict[zip]["North"] = line[6]
            else:
                count += 1
        f.close()

    def zipcodes_append(self, key, value):
        self.zipcodes[key] = value

    def zipcodes_get(self, key):
        return self.zipcode_dict.get(key)

    def create_link(self):
        url = "https://www.zillow.com/homes/" + self.ID
        return url

    def parse_json(self):
        print("Found the json api")

    def append_to_file(self):
        # try:
        f = open("zipcodes.txt","a")
        #TODO Append to the end of the file
        regionID,regionType,west,east,south,north = self.locate_id(self.zipcode)
        new_line = "{} {} {} {} {} {} {}\n".format(self.zipcode,regionID,regionType,west,east,south,north)
        f.write(new_line)
        f.close()
        # except:
        #     print("Error appending into file")

    def locate_id(self,zipcode):
        def remove_garbage_symbols(data):
            data = data.replace("\"","")
            data = data.replace("{","")
            data = data.replace("}","")
            data = data.replace("[","")
            data = data.replace("]","")
            data = data.replace("\n","")
            data = data.replace("regionSelection:","")
            return data
        #TODO Go onto zillow and find the unique id for the zipcode
        url = "https://www.zillow.com/homes/" + zipcode+"_rb"
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                   'Accept-Encoding': 'identity'
                   }
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.content,'lxml')
        data = str(soup.find('script',{"data-zrr-shared-data-key":"mobileSearchPageStore"}))
        data = remove_garbage_symbols(data)
        north = ""
        south = ""
        east = ""
        west = ""
        regionType = ""
        regionID = ""
        counter = 0

        def match_coordinates(expression):
            try:
                # groups = re.findall('(-*[0-9]+.[0-9]+)',expression)
                # for x in groups:
                #     print(x)
                return re.search('(-*[0-9]+.[0-9]+)',expression).group(0)
            except:
                return False


        for x in data.split(","):
            #print(x)
            if re.match("north",x) != None  and match_coordinates(x) != False:
                north = match_coordinates(x)

            if re.match("west",x) != None  and match_coordinates(x) != False:
                west = match_coordinates(x)

            if re.match("south",x) != None  and match_coordinates(x) != False:
                south = match_coordinates(x)


            if re.match("east",x) != None  and match_coordinates(x) != False:
                east = match_coordinates(x)


            if re.match("regionId",x) != None and match_coordinates(x) != False and counter == 0:
                regionID = match_coordinates(x)
                counter += 1
            if re.match("regionType",x) != None:
                try:
                    regionType = re.search("([0-9]+)",x).group(0)
                except:
                    pass
        return regionID,regionType,west,east,south,north

    def generate_link(self):
        regionID = self.zipcode_dict[self.zipcode]["RegionID"]
        regionType =  self.zipcode_dict[self.zipcode]["RegionType"]
        west = self.zipcode_dict[self.zipcode]["West"]
        east = self.zipcode_dict[self.zipcode]["East"]
        south = self.zipcode_dict[self.zipcode]["South"]
        north = self.zipcode_dict[self.zipcode]["North"]
        # url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={{\"pagination\":{{}},\"usersSearchTerm\":\"{}\",\"mapBounds\":{{\"west\":{},\"east\":{},\"south\":{},\"north\":{} }},\"regionSelection\":[{{\"regionId\":{},\"regionType\":{} }}],\"isMapVisible\":true,\"filterState\":{{\"sortSelection\":{{\"value\":\"globalrelevanceex\"}},\"isAllHomes\"" \
        #       ":{{\"value\":true}}}},\"isListVisible\":true,\"mapZoom\":13}}&wants={{\"cat1\":[\"mapResults\"]}}&requestId=2".format(self.zipcode,west,east,south,north,regionID,regionType)
        url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={{\"pagination\":{{}},\"usersSearchTerm\":{} ," \
              "\"mapBounds\":{{\"west\":{},\"east\":{},\"south\":{},\"north\":{}}},\"regionSelection\":[{{\"regionId\":{}," \
              "\"regionType\":{} }}],\"isMapVisible\":true,\"filterState\":{{\"isForSaleByAgent\":{{\"value\":{}}}," \
              "\"isForSaleByOwner\":{{\"value\":{} }},\"isNewConstruction\":{{\"value\":false}},\"isForSaleForeclosure\":{{\"value\":{}}}," \
              "\"isComingSoon\":{{\"value\":false}},\"isAuction\":{{\"value\":{} }},\"isPreMarketForeclosure\":{{\"value\":{} }}," \
              "\"isPreMarketPreForeclosure\":{{\"value\":false}},\"isForRent\":{{\"value\":{}}},\"isAllHomes\":{{\"value\":true}}}}," \
              "\"isListVisible\":true,\"mapZoom\":12}}&wants={{\"cat1\":[\"mapResults\"]}}&requestId=2".format(self.zipcode,west,east,south,north,regionID,regionType,self.fsba,self.fsbo,self.foresale,self.forAuction,self.premarket,self.rent)
        return url





# zipcode = input("What zipcode do you want to look up?: ")
# test = Property_Grab(zipcode)
# test.read_file()
# if test.zipcodes_get(zipcode) != None:
#     print(test.generate_link())
# else:
#     test.append_to_file()
# # test.locate_id(zipcode)


