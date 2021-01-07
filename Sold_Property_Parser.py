import requests
from Sold_Property import Sold_Property
from datetime import datetime
from database import sql
import re
class Sold_Parser:
    def __init__(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
            'Accept-Encoding': 'identity'
        }
        response = requests.get(url, headers=headers)
        self.house_data = response.json()["cat1"]["searchResults"]["mapResults"]

    def get_bed(self,data):
        try:
            return data["beds"]
        except:
            return -1

    def get_bath(self,data):
        try:
            return data["baths"]
        except:
            return -1

    def get_area(self,data):
        try:
            return data["area"]
        except:
            return -1

    def get_lat_long(self,data):
        try:
            return [data["latLong"]["latitude"],data["latLong"]["longitude"]]
        except:
            return -1

    def get_sold_date(self,data):
        try:
            epoch_time = str(data["hdpData"]["homeInfo"]["dateSold"])
            date = datetime.fromtimestamp(int(epoch_time[:-3])).strftime('%Y-%m-%d')
            return date
        except KeyError:
            return -1

    def get_zestimate(self,data):
        try:
            return data["hdpData"]["homeInfo"]["zestimate"]
        except:
            return -1

    def get_price(self,data):
        try:
            return data["hdpData"]["homeInfo"]["price"]
        except:
            return -1

    def get_zid(self,data):
        try:
            return data["hdpData"]["homeInfo"]["zpid"]
        except:
            return -1

    def get_zipcode(self,data):
        try:
            return data["hdpData"]["homeInfo"]["zipcode"]
        except:
            return -1

    def get_rent_zestimate(self,data):
        try:
            return data["hdpData"]["homeInfo"]["rentZestimate"]
        except:
            return -1

    def get_address(self,data):
        try:
            address = re.search("(\d+-\D+)",data["detailUrl"]).group(1)
            address = address.replace("-"," ")
            return address[:-1]
        except:
            return -1

    def parse_link(self):
        count = 0
        db = sql()
        for x in self.house_data:
            bed = self.get_bed(x) if self.get_bed(x) != -1 else None
            bath = self.get_bath(x) if self.get_bath(x) != -1 else None
            sqft = self.get_area(x) if self.get_area(x) != -1 else None
            lat,long = self.get_lat_long(x) if (self.get_lat_long(x)[0] != -1 or self.get_lat_long(x)[0] != -1) else None
            sold_date = self.get_sold_date(x) if self.get_sold_date(x) != -1 else None
            zestimate = self.get_zestimate(x) if self.get_zestimate(x) != -1 else None
            price = self.get_price(x) if self.get_price(x) != -1 else None
            zid = self.get_zid(x) if self.get_zid(x) != -1 else None
            rent_zestimate = self.get_rent_zestimate(x) if self.get_rent_zestimate(x) != -1 else None
            address = self.get_address(x) if self.get_address(x) != -1 else None
            zipcode = self.get_zipcode(x) if self.get_zipcode(x) != -1 else None


            if bed != -1 and bath and -1 and sqft != -1 and address != -1 and db.check_property(zid,"sold_houses") is None:
                query = "INSERT INTO sold_houses (zid, Latitude, Longitude, Bed, Bath, Sqft, Zestimate,`Rent Zestimate`, Price, " \
                        "zipcode, address, `sold date`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                        "'{}','{}', '{}')".format(zid, lat, long, bed, bath, sqft, zestimate, rent_zestimate,price, zipcode, address,sold_date)
                db.run_insert_query(query)
                count+=1
        db.close()
        print("Successfully inserted: {} into database".format(count))

url = Sold_Property("80016").generate_link()
print(url)
test = Sold_Parser(url).parse_link()