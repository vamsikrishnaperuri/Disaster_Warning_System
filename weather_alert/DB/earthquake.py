# Disaster Warning System

import requests
from datetime import datetime
import math
import variables as var
import time
import geolocation as geo
import MakeCall as mk


def haversineDistance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # Calculate the result
    print("Haversine Distance : ", c * r)
    return c * r


def clearEarthquakeData():
    alerts = var.alerts
    for __city in alerts.keys():
        alerts[__city]['earthquake'] = ""
    return alerts


def checkCity(list1, _city):
    for ele in list1:
        if _city in ele:
            return ele
    return False


def calculateImpactArea(m):
    if m > 9.5:
        return 30000
    elif m > 9.0:
        return 20000
    elif m > 8.5:
        return 10000
    elif m > 8.0:
        return 5000
    elif m > 7.5:
        return 2000
    elif m > 7.0:
        return 1000
    elif m > 6.5:
        return 500
    elif m > 6.0:
        return 400
    elif m > 5.5:
        return 360
    elif m > 5.0:
        return 300
    elif m > 4.5:
        return 200
    elif m > 4.0:
        return 150
    elif m > 3.5:
        return 100
    else:
        return 0


# noinspection PyShadowingNames
def getEarthquakeData():
    alerts = var.alerts
    to_call_list = set()
    url = rf"https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {'format': 'geojson', 'starttime': str(datetime.now())[:10]}
    resp = requests.get(url=url, params=params)
    print(resp.url)
    clearEarthquakeData()
    data = resp.json()
    status = resp.status_code
    if status == 200:
        if data is []:
            pass
        else:
            i = 0
            earthquake_data = {}
            length = len(data['features'])
            print(length)
            present_time = time.time()
            while i < length:
                magnitude = data['features'][i]['properties']['mag']
                location = data['features'][i]['properties']['place']
                quakecoordinates = (data['features'][i]['geometry']['coordinates'])
                etime = data['features'][i]['properties']['updated']
                if magnitude <= 3.5 and present_time - etime > 15:  # magnitude less than 4.5 and time less than 45 sec (Max alert time 45s)
                    pass
                else:
                    earthquake_data[location] = [quakecoordinates, magnitude]
            print(earthquake_data)
            # All the cities affected by earthquake are gathered
            coordinates = var.coordinates
            for city in coordinates.keys():
                for location in earthquake_data.keys():
                    quakecoordinates = earthquake_data[location][0]
                    impactArea = calculateImpactArea(earthquake_data[1])
                    if haversineDistance(quakecoordinates[1], quakecoordinates[0], coordinates[city][0],
                                         coordinates[city][1]) < impactArea:
                        if alerts[city]['earthquake'] == '':
                            alerts[city][
                                'earthquake'] += f"Caution! Earthquake detected/passed at {city}. Follow Precautions"
                        else:
                            alerts[city][
                                'earthquake'] += f"Caution! Multiple Earthquakes detected/passed at {city}. Follow Precautions"
                        to_call_list.add(geo.convertCoordinatesToCity(quakecoordinates[1], quakecoordinates[0]))

    to_call_list = to_call_list - var.old_to_call_earthquake_list
    earthquake_call_string = f"Earthquakes detected at {','.join(to_call_list)}"
    mk.completeProcess(earthquake_call_string)
    var.old_to_call_earthquake_list = to_call_list
    # Edit the changes back
    var.alerts = alerts

