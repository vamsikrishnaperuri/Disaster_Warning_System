# This module is related to all information regarding the accuweather api
# Only the apikey
import requests
import variables as var

accuweather_apikey = "YOUR_API_KEY"
period = "5day"


def convertCityToKey(city):
    city.capitalize()
    city_key = ""
    url = "http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {'apikey': accuweather_apikey, 'q': city}
    resp = requests.get(url=url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        city_key = data[0]['Key']
        print(city, city_key)
    else:
        print("Error", resp.status_code)
    return city_key


def getWeatherAlerts(locationkey):
    global period
    url = f"http://dataservice.accuweather.com/alarms/v1/{period}/{locationkey}"
    params = {'apikey': accuweather_apikey}
    resp = requests.get(url=url, params=params)
    report = ""
    if resp.status_code == 200:
        data = resp.json()
        # print(data)
        if data == []:
            pass
        else:
            length = len(data["Alerts"])
            if length != 0:
                for i in range(length):
                    disastertype = data['Alerts'][i]["Type"]
                    severity = data['Alerts'][i]["Severity"]
                    starttime = data['Alerts'][i]["StartTime"]
                    endtime = data['Alerts'][i]["EndTime"]
                    report += f"{disastertype} {severity} from {starttime} till {endtime}\n"
            else:
                pass
    elif resp.status_code == 401 or resp.status_code == 403:
        raise Exception("API Error - Accuweather API Key is invalid")
    return report


def getAllWeatherAlerts():
    for locationkey in var.city_keys.keys():
        report = getWeatherAlerts(locationkey)
        var.alerts[var.city_keys[locationkey]]['accuweather'] = report
    return True


