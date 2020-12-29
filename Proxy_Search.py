import requests
from bs4 import BeautifulSoup
import json
import re
class Proxy_Search():

    def find_link(self):

        headers = {
            "apikey": "734a7cf0-48c1-11eb-98ca-476fc1ac07bc"
        }

        params = (
            ("url","https://www.zillow.com/homedetails/24552-E-Easter-Pl-Aurora-CO-80016/54644111_zpid/"),
        );

        response = requests.get('https://app.zenscrape.com/api/v1/get', headers=headers, params=params);
        print(response.text)

class Find_Property_Details():
    def __init__(self,zid):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                   'Accept-Encoding': 'identity'
                   }
        url = "https://www.zillow.com/homedetails/{}_zpid/".format(zid)
        response = requests.get(url,headers = headers)
        #print(response.text)
        soup = BeautifulSoup(response.content,'lxml')
        #self.data = soup.find('script', {"data-zrr-shared-data-key":"mobileSearchPageStore"}).string
        self.data = soup


    def parse_data(self):
        def is_wanted_data(text):
            if "Year built" in text:
                return 1
            elif "Major remodel year" in text:
                return 2
            elif "HOA fee" in text:
                return 3
            elif "Heating features" in text:
                return 4
            return -1

        all_tags = self.data.find_all(class_="Text-c11n-8-18-0__aiai24-0 foiYRz")
        year_built = ""
        hoa_fee = ""
        major_remodel_year = ""
        heating = ""
        for x in all_tags:
            result = is_wanted_data(x.get_text())
            #print(x.get_text())
            if result == 1:
                year_built = re.search("(\d+)",x.get_text()).group(1)
            elif result == 2:
                major_remodel_year = re.search("(\d+)",x.get_text()).group(1)
            elif result == 3:
                hoa_fee = re.search("(\$\w+/\w+)",x.get_text()).group(1)
            elif result == 4:
                print(x.get_text())
                try:
                    heating = re.findall("(\w+ \w+)",x.get_text())[1]
                except:
                    heating = "-1"

        return year_built,major_remodel_year,hoa_fee,heating
        print(f"Year Built: {year_built} \n Remodeled: {major_remodel_year} \n HOA Fee: {hoa_fee} \n Heating {heating}")



# url = "https://www.zillow.com/homedetails/24552-E-Easter-Pl-Aurora-CO-80016/54646742_zpid/"
# test =  Find_Property_Details(url)
# test.parse_data()