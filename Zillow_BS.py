from bs4 import BeautifulSoup
import requests
class Test:
    def __init__(self):
        print("Inside init")
    def createvar(self):
        self.newVar = "Hello"
    def testVar(self):
        print(self.newVar)


newVar = Test()
newVar.createvar()
newVar.testVar()
#
# url = 'https://www.zillow.com/homes/80016/'
# # header='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
           'Accept-Encoding': 'identity'
           }
#
# response = requests.get(url,headers=headers)
# soup = BeautifulSoup(response.content,'lxml')
# print(soup.prettify())

