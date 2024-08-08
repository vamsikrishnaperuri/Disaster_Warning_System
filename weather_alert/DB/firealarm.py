# This module is completely used to detect and update the server of any fire

import variables as var
import newcity as nc
import time


def updateFireAlert(uid, value, cityname):
    report = f"Fire at {uid} is {value} - {int(time.time())}"
    if cityname in var.cities:
        var.alerts[cityname]['fire'] = report
    else:
        if nc.newCity(cityname):
            var.alerts[cityname]['fire'] = report
    return True


def clearFireAlert():
    time_now = int(time.time())
    for city in var.cities:
        data = var.alerts[city]['fire']
        newdata = ""
        if data != '':
            data = data.split('\n')
            for line in data:
                pasttime = int(line[-10:])
                if time_now - pasttime < 15:
                    newdata += line
                else:
                    pass
            var.alerts[city]['fire'] = newdata
    print("Fire Data Cleared")
