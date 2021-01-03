import mysql.connector
from mysql.connector import errorcode
from datetime import date

# Finding how much memory it takes https://stackoverflow.com/questions/6474591/how-can-you-determine-how-much-disk-space-a-particular-mysql-table-is-taking-up
class sql:

    def __init__(self):
        try:
            self.read_config()
            self.mydb = mysql.connector.connect(user='admin', password=self.pw,
                                                host=self.db_link, database="real_estate")
            self.db_link = ""
            self.pw = ""
            # print("success")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        self.mydb.close()

    def read_config(self):
        f = open("database/config.txt")
        count = 0
        for x in f:
            if count == 0:
                self.db_link = x
            elif count == 1:
                self.pw = x
            count += 1

    def insert_property(self, property_data):
        count = 0
        for x in property_data:
            if x == "":
                property_data[count] = None
            count += 1
        zid = int(property_data[0])
        lat = property_data[1]
        long = property_data[2]
        bed = float(property_data[3]) if property_data[3] != "None" else None
        print(property_data[4], zid)
        bath = float(property_data[4]) if property_data[4] != "None" else None
        sqft = int(property_data[5]) if property_data[5] is not None else None
        zestimate = int(property_data[6]) if property_data[6] is not None else None
        price = float(property_data[7]) if property_data[7] is not None else None
        hoa = property_data[8]
        year_built = int(property_data[9]) if property_data[9] is not None else None
        year_remodel = int(property_data[10]) if property_data[10] is not None else None
        heating = property_data[11]
        status = property_data[12]
        zipcode = int(property_data[13]) if property_data[13] is not None else None
        address = property_data[14]
        cursor = self.mydb.cursor()
        query = "INSERT INTO real_estate (zid, Latitude, Longitude, Bed, Bath, Sqft, Zestimate, Price, " \
                "HOA, `Year Built`, `Remodel Year`, Heating,status, zipcode, address, `inserted date`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                "'{}','{}','{}','{}','{}','{}', '{}')".format(zid, lat, long, bed, bath, sqft, zestimate, price, hoa,
                                                        year_built, year_remodel, heating, status, zipcode, address,date.today())
        # cursor.execute("INSERT INTO real_estate (zid, Latitude, Longitude, Bed, Bath, Sqft, Zestimate, Price, HOA, Year Built, Remodel Year, Heating, zipcode, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(zid,lat,long,bed,bath,sqft,zestimate,price,hoa,year_built,year_remodel,heating,zipcode,address))
        cursor.execute(query)
        cursor.close()
        self.mydb.commit()

    def insert_zipcodes(self, zipcode_data):
        sql_query = """
        INSERT INTO zipcodes (zipcode,`region id`, `region type`, west, east, south, north)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        print(zipcode_data)
        cursor = self.mydb.cursor()
        cursor.execute(sql_query, zipcode_data)
        cursor.close()
        self.mydb.commit()

    def check_zipcode(self, zipcode):
        cursor = self.mydb.cursor()
        query = """
        SELECT zipcode,`region id`, `region type`, west, east, south, north FROM zipcodes WHERE zipcode = {}
        """.format(zipcode)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return result
        return None

    def check_property(self, zid):
        cursor = self.mydb.cursor()
        query = """
        select zid from real_estate where zid = {}
        """.format(zid)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return result
        return None

    # def insertStoreEntry(self,store_id,sku,price,exist,location):
    #     cursor = self.mydb.cursor()
    #     query = "INSERT INTO Walmart{} (sku, Price, availability, location) VALUES ('{}',{},{},'{}')".format(store_id,sku,price,exist,location)
    #     print("Successfully inserted Walmart{} with SKU={} entry".format(store_id,sku))
    #     cursor.execute(query)
    #     cursor.close()
    #     self.mydb.commit()


test = sql()
