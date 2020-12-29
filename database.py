import mysql.connector
from mysql.connector import errorcode

#Finding how much memory it takes https://stackoverflow.com/questions/6474591/how-can-you-determine-how-much-disk-space-a-particular-mysql-table-is-taking-up
class sql:

    def __init__(self):
        try:
            self.read_config()
            self.mydb = mysql.connector.connect(user = 'admin', password = self.pw,
                                                host = self.db_link, database = "real_estate")
            print("success")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
    def read_config(self):
        f = open("database/config.txt")
        count = 0
        for x in f:
            if count == 0:
                self.db_link = x
            elif count == 1:
                self.pw = x
            count += 1

test = sql()
