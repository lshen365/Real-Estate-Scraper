import requests
import re
from Proxy_Search import Find_Property_Details
from database import sql
from datetime import date

class For_Sale:
    def __init__(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
            'Accept-Encoding': 'identity'
        }
        response = requests.get(url, headers=headers)
        self.property_json = response.json()
        self.write_first_line()

    def get_property_list(self):
        return self.property_json["cat1"]["searchResults"]["mapResults"]

    def get_zid(self,dict):
        return dict["zpid"]

    def get_long(self, dict):
        return dict["latLong"]["longitude"]

    def get_lat(self, dict):
        return dict["latLong"]["latitude"]

    def get_price(self, dict):
        return dict["hdpData"]["homeInfo"]["price"]

    def get_zillow_sale_price(self, dict):
        return dict["hdpData"]["homeInfo"]["zestimate"]

    def get_zillow_rent_price(self, dict):
        return dict["hdpData"]["homeInfo"]["rentZestimate"]

    # def get_is_FSBA(self, dict):
    #     # None means cannot be found
    #     try:
    #         return dict["hdpData"]["homeInfo"]["listing_sub_type"]["is_FSBA"]
    #     except:
    #         return None

    def get_address(self, dict):
        address = re.search('([0-9]+-\w+-\w+-\w+-\w+)', dict["detailUrl"]).group(1)
        return address

    def get_bed(self, dict):
        return dict["beds"]

    def get_baths(self, dict):
        return dict["baths"]

    def get_sqft(self, dict):
        return dict["area"]

    def get_home_status(self, dict):
        return dict["hdpData"]["homeInfo"]["homeStatus"]

    def get_zipcode(self, dict):
        return dict["hdpData"]["homeInfo"]["zipcode"]

    def get_rent_zestimate(self, dict):
        return dict["hdpData"]["homeInfo"]["rentZestimate"]

    def write_first_line(self):
        f = open("properties_data.txt", "w")
        f.write("ADDRESS | LAT | LONG | BED | BATH | SQFT | ZESTIMATE | Price | FSBA | HOME_STATUS | ZID \n")

    def append_to_file(self, information):
        line = ""
        for x in information:
            line += x + " "
        line = line[:-1] + "\n"
        f = open("properties_data.txt", "a")
        f.write(line)
        f.close()

    def interate_thru_property(self):

        properties = self.get_property_list()
        for x in properties:
            try:
                zid = str(self.get_zid(x))  # Produced an error
                db = sql()
                if db.check_property(zid,"real_estate") is None:
                    price = str(self.get_price(x))

                    longitude = str(self.get_long(x))
                    latitude = str(self.get_lat(x))
                    zillow_sale_price = str(
                        self.get_zillow_sale_price(x))  # Produces an error for Lots/Land or when Zillow Estimate = None
                    address = self.get_address(x)
                    bed = str(self.get_bed(x))  # Returns errors on buildings
                    bath = str(self.get_baths(x))  # Return errors on buildings
                    sqft = str(self.get_sqft(x))  # Return errors on buildings
                    home_status = str(self.get_home_status(x))  # Return errors on buildings
                    zipcode = self.get_zipcode(x)
                    year_built, major_remodel, hoa, heating = Find_Property_Details(zid).parse_data()
                    result = [zid, latitude, longitude, bed, bath, sqft, zillow_sale_price, price, hoa, year_built,
                              major_remodel, heating, home_status, zipcode, address]
                    print("Added Property")
                    db.insert_property(result)

                db.close()



            except KeyError:
                pass

    # def get_long(self):
    #
    # def get_lat:
    #
    # def get_zillow_estimate:

# url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={\"pagination\":{},\"usersSearchTerm\":\"80016\",\"mapBounds\":{\"west\":-104.871333,\"east\":-104.642013,\"south\":39.551088,\"north\":39.652876 },\"regionSelection\":[{\"regionId\":93206,\"regionType\":7 }],\"isMapVisible\":true,\"filterState\":{\"sortSelection\":{\"value\":\"globalrelevanceex\"},\"isAllHomes\":{\"value\":true}},\"isListVisible\":true,\"mapZoom\":13}&wants={\"cat1\":[\"mapResults\"]}&requestId=2"
# test = For_Sale(url)
# test.interate_thru_property()
