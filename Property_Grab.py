from bs4 import BeautifulSoup
import requests
import json
from database import sql


class Property_Grab:
    def __init__(self,zip,filters):
        # self.set_up_proxy()
        self.zipcode = zip
        self.zipcode_dict = {}
        self.rent, self.fsba, self.fsbo, self.forAuction, self.foresale, self.premarket = filters

    def zipcodes_get(self, key):
        """
        Checks if the zipcode exists in the database
        :param key: zipcode of the location
        :type key: string
        :return: True if zipcode found, False if zipcode not found
        :rtype: Bool
        """
        db = sql()
        if db.check_zipcode(key) is not None:
            results = db.check_zipcode(key)
            self.regionID = results[1]
            self.regionType = results[2]
            self.west = results[3]
            self.east = results[4]
            self.south = results[5]
            self.north = results[6]
            db.close()
            return True
        db.close()
        return False

    def add_to_database(self):
        regionID,regionType,west,east,south,north,city,county = self.locate_id(self.zipcode)
        results = (int(self.zipcode),int(regionID),int(regionType),west,east,south,north)
        db = sql()
        db.insert_zipcodes(results)
        db.close()

    def locate_id(self,zipcode):

        def remove_garbage_symbols(data):
            data = data.replace("<","")
            data = data.replace(">","")
            data = data.replace("!","")
            return data

        url = "https://www.zillow.com/homes/" + zipcode+"_rb"
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                   'Accept-Encoding': 'identity'
                   }
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.content,'lxml')
        try:
            data = soup.find('script',{"data-zrr-shared-data-key":"mobileSearchPageStore"}).string

            data = remove_garbage_symbols(data)
            data = data[2:-2] #Removes the -- at the beginning and end
            data_json = json.loads(data)
            north = data_json['queryState']['mapBounds']['north']
            south = data_json['queryState']['mapBounds']['south']
            east = data_json['queryState']['mapBounds']['east']
            west = data_json['queryState']['mapBounds']['west']
            regionType = data_json['queryState']['regionSelection'][0]['regionType']
            regionID = data_json['queryState']['regionSelection'][0]['regionId']
            city = data_json['searchPageConstants']['gtm']["gtmInitialData"][1]['gaCustomDimensions']['dimension5']
            county = data_json['searchPageConstants']['gtm']["gtmInitialData"][1]['gaCustomDimensions']['dimension4']
            return regionID,regionType,west,east,south,north,city,county
        except KeyError as e:
            print("Could not find " + str(e))

    def generate_link(self):
        regionID = self.regionID
        regionType =  self.regionType
        west = self.west
        east = self.east
        south = self.south
        north = self.north
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
# test.locate_id(zipcode)
# test.read_file()
# if test.zipcodes_get(zipcode) != None:
#     print(test.generate_link())
# else:
#     test.append_to_file()
# test.locate_id(zipcode)


