# Disaster Warning System
# Framework - Falcon

# We will get coordinates from the user

import variables as var
import earthquake as eq
import accuweather as accu
import firealarm as fa
import geolocation as geo
import newcity as nc
import Twillio
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)


# noinspection PyBroadException
@app.route('/fetchData')
def getData():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    print(lat, lng)
    try:
        city = geo.convertCoordinatesToCity(lat, lng)
        print(city)
        if city in var.cities:
            return var.alerts[city]
        else:
            res = nc.newCity(city)
            if res:
                return var.alerts[city]
            else:
                return "Some Error Has Occurred"
    except Exception:
        return "Unable to fetch Location"


@app.route('/firealarm')
def fireAlert():
    uid = request.args.get("uid")
    value = request.args.get("value")
    city = request.args.get("city")
    print(city, uid, value)
    fa.updateFireAlert(uid, value, city)
    return {'status': 'successful', 'statusCode': 200}


@app.route('/')
def displayHelloMessage():
    string = "The Server is Running... "
    return string


accuweather_scheduler = BackgroundScheduler()
accuweather_scheduler.add_job(func=accu.getAllWeatherAlerts, trigger="interval", hours=96)
accuweather_scheduler.start()
earthquake_scheduler = BackgroundScheduler()
earthquake_scheduler.add_job(func=eq.getEarthquakeData, trigger="interval", seconds=10)
earthquake_scheduler.start()
firealarm_scheduler = BackgroundScheduler()
firealarm_scheduler.add_job(func=fa.clearFireAlert, trigger="interval", seconds=15)
firealarm_scheduler.start()

if __name__ == "__main__":
    print("Server Started")
    app.run(host="0.0.0.0", port=8000)
