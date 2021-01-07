from database import sql
class Sold_Property:
    def __init__(self,zipcode):
        self.zipcode = zipcode

    def get_directions(self):
        query = """
        select `Region ID`, `Region Type`, West, East, South, North FROM zipcodes where zipcode = %s;
        """ % (self.zipcode)
        db = sql()
        result = list(db.run_query_with_results(query)[0])
        self.region_id = result[0]
        self.region_type = result[1]
        self.west = result[2]
        self.east = result[3]
        self.south = result[4]
        self.north = result[5]
    def generate_link(self):
        self.get_directions()

        url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={{\"pagination\":{{}},\"usersSearchTerm\":{}," \
              "\"mapBounds\":{{\"west\":{},\"east\":{},\"south\":{},\"north\":{}}},\"regionSelection\":[{{\"regionId\":{},\"regionType\":{} }}]," \
              "\"isMapVisible\":true,\"filterState\":{{\"isForSaleByAgent\":{{\"value\":false}},\"isForSaleByOwner\":{{\"value\":false}},\"isNewConstruction\":{{\"value\":false}},\"isForSaleForeclosure\":{{\"value\":false}},\"isComingSoon\":{{\"value\":false}},\"isAuction\":{{\"value\":false}},\"isPreMarketForeclosure\":" \
              "{{\"value\":false}},\"isPreMarketPreForeclosure\":{{\"value\":false}},\"isRecentlySold\":{{\"value\":true}},\"isAllHomes\":{{\"value\":true}},\"isSingleFamily\":" \
              "{{\"value\":false}},\"isTownhouse\":{{\"value\":false}}}},\"isListVisible\":true,\"mapZoom\":12}}&wants={{\"cat1\":[\"mapResults\"]}}&requestId=2".format(self.zipcode,self.west,self.east,self.south,self.north,self.region_id,self.region_type)
        return url

# test = Sold_Property(80016)
# test.generate_link()