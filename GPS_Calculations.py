from math import radians, cos, sin, asin, sqrt

class GPS():

    #Haversines formula for calculating distance between two lat/long coordinates
    def haversine(self,lat1, lon1, lat2, lon2):

        R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))

        return R * c

test = GPS()
print(test.haversine(39.596250,-104.783060,39.599620,-104.783000))
