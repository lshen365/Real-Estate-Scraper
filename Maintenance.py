from database import sql
from datetime import date
class Clean:

    def __init__(self):
        self.db = sql()

    def clean_old_dates(self):
        query = """
        SELECT zid  FROM real_estate WHERE DATEDIFF (NOW(),`inserted date`) > 1; 
        """
        self.db.run_query_with_results(query,None)


test = Clean()
test.clean_old_dates()