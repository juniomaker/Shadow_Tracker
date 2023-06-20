"""
    This API will be consumed by another part of the application,
    providing the data to generate the graphs

    data structure:
   
{'azimuth': 245.935,
 'azimuth_shadow': 65.935, 
 'coord_x_azimuth_shadow': 37.3781, 
 'coord_y_azimuth_shadow': 83.6969, 
 'day': 3,
 'elevation': 0.702,
 'month': 12,
 'ray': 91.664, 
 'time': (18, 20, 0)}

"""

import math
from pprint import pprint
import time
from ext.sunpos import sunpos, into_range

pi = math.pi
sin = math.sin
cos = math.cos
rad, deg = math.radians, math.degrees

# set parameters 
hours = range(6, 19)
days = range(1, 2)
months = range(1, 13)
year = 2023
time_zone = -3
location = (-22.814519, -42.940407)

# creates a list of tuples with the values of time, zimuth, and elevation

positions = list()
for month in months:
    
    for day in days:
        for hour in hours:
            for minuts in range(0, 60, 10):
                for sec in range(0, 60, 60):
                    when = (year, month, day, hour, minuts, sec, time_zone)
                    azimuth, elevation = sunpos(when, location, True)
                    if not elevation <= 0:
                        positions.append(
                            {
                            'month': month,
                            'day': day,
                            'time': (hour, minuts, sec),
                            'azimuth': azimuth,
                            'elevation':elevation
                            }
                        )
            
    

#returns the value of the adjacent leg based on the elevation angle and value of the opposite leg
def ca(co, ang):
    if ang == 90:
        return 0
    if ang < 1:
        ang = 1
    tangente = math.tan(rad(ang))
    pos_ca = co/tangente
    return round(pos_ca, 3)

ang = list()
y = list()


for position in positions:
    position['azimuth_shadow'] = round(into_range(position['azimuth'] + 180, 0, 360), 4)
    position['ray'] = ca(1.6, (position['elevation']))
    position['coord_y_azimuth_shadow'] = round(sin(rad(position['azimuth_shadow']))*position['ray'], 4)
    position['coord_x_azimuth_shadow'] = round(cos(rad(position['azimuth_shadow']))*position['ray'], 4)

if __name__ == "__main__":
    for pos in positions:
        if pos['time'][0] == 18:
            pprint(pos)
