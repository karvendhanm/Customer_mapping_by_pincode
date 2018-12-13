from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

lat1 = radians(11.245)
lon1 = radians(77.6114)
lat2 = radians(13.0381)
lon2 = radians(77.6549)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result:", distance)


import pgeocode
nomi = pgeocode.Nominatim('in')
print(dist.query_postal_code("638106","560034"))




