# This module will handle any new city into the program

import variables as var
import geolocation as geo
import accuweather as accu
import earthquake as eq


def newCityCoordinates(lat, lng):
    city = geo.convertCoordinatesToCity(lat, lng)
    if city == '':
        print("City Unrecognizable.")
        return False
    else:
        print(city)
        city_coordinates = geo.convertCityToCoordinates(city)
        key = accu.convertCityToKey(city)
        var.cities.append(city)
        var.coordinates[city] = city_coordinates
        var.city_keys[key] = city
        var.alerts[city] = {'earthquake': '', 'accuweather': '', 'fire': ''}
        # Update the Earthquake and Accuweather data
        var.alerts[city]['accuweather'] = accu.getWeatherAlerts(key)
        eq.getEarthquakeData()
        return city


def newCity(city):
    try:
        city_coordinates = geo.convertCityToCoordinates(city)
        key = accu.convertCityToKey(city)
        var.cities.append(city)
        var.coordinates[city] = tuple(city_coordinates)
        var.city_keys[key] = city
        var.alerts[city] = {'earthquake': '', 'accuweather': '', 'fire': ''}
        # Update the Earthquake and Accuweather data
        var.alerts[city]['accuweather'] = accu.getWeatherAlerts(key)
        # eq.getEarthquakeData()
        return True
    except Exception as e:
        print(e)
        return False


