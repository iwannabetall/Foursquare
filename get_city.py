#!/usr/bin/python # -*- coding: utf-8 -*-
from unidecode import unidecode
#reverse geocoding - given a lat/long, get the city
from urllib2 import urlopen
import json
import os
import pandas as pd 
from time import sleep

##reverse geocode-get city from lat/long.  thanks google and stackoverflow! 
def getplace(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']  #long json formatted data
    city = state = None
    for c in components:
        ##get city
        if "locality" in c['types']:  
            city = c['long_name'].encode('utf-8')
        #state or province?
        if "political" in c['types'] and "administrative_area_level_1" in c['types']:
            state = c['long_name'].encode('utf-8')
    return city, state

#trying to minimize comparisons, return if match    
def find_match(longitude,latitude,places, often_frequented_place):
    for j in range(len(latitude)):
        if often_frequented_place == places[j]:
            print "match" + str(j)
            return latitude[j],longitude[j]
            #oft_long1 = longitude[j]
            #oft_lat1 = latitude[j]
            #return oft_lat1, oft_long1            

def main():
    fsq_data = pd.read_csv("FOURSQUARE_DATA_With_Local_Times.csv",sep = ',')

    places = fsq_data["Place"]
    latitude = fsq_data["Latitude"]
    longitude = fsq_data["Longitude"]
    ##for places with most frequent queries, google reverse geotag once
    often_frequented = ["NBA HQ", "Dillon Gym", "Facebook HQ", "Homestead Park Aquatic Center", "Avery Recreation Pool", "Raleigh-Durham International Airport",
    "Banh Mi Saigon Bakery", "Sherrerd Hall", "LaGuardia Airport (LGA)", "Barclays Center", "John F. Kennedy International Airport (JFK)", "Madison Square Garden", 
    "Arrillaga Outdoor Education and Recreation Center", "Palo Alto Caltrain Station", "The Kalahari", "Harris Teeter", "New York Penn Station", "San Francisco Caltrain Station",
    "BCD Tofu House", "Chapel Hill Public Library", "Frist Campus Center", "Palmer House - a Hilton Hotel", "Chicago O'Hare International Airport", "Princeton University", "Anna's Bakery", 
    "Bill's Bar & Burger", "J.P. Licks", "MIT Sloan Sports Analytics Conference", "Northwestern Memorial Hospital", "Quest Multisport", "San Francisco International Airport (SFO)", 
    "Sunshine 27 Seafood Restaurant", "The Bent Spoon", "Toyota Center", "AMC Southpoint 17", "Friend Center", "GT Fish and Oyster", "InterContinental Chicago Magnificent Mile", "Kang Suh",
    "Los Tacos No.1", "Num Pang Sandwich Shop", "Nyonya", "Oak Creek Apartments", "Smorgasburg Williamsburg", "99 Ranch Market", "Arrillaga Center for Sports & Recreation", 
    "Boston Convention & Exhibition Center", "Central Park", "Chelsea Piers Sports Center", "Dod Hall", "Dropbox HQ", "Ferry Plaza Farmers Market", "Hyatt Regency New Orleans", 
    "Jane", "JW Marriott", "Kenan Memorial Stadium", "National September 11 Memorial & Museum", 
    "Philz Coffee", "Pudong Shangri-La Hotel", "Stanford University", "The Root Cellar Cafe & Catering", "Totto Ramen", "U.S. Athletic Training Center", "Wyndham Grand Rio Mar Beach Resort & Spa",
    "Co.","Cocoron","Communiversity","Dean E. Smith Center","Delicious Dim Sum","Detroit Metropolitan Wayne County Airport (DTW)","George R. Brown Convention Center","Good Mong Kok Bakery",
    "Hilton Americas-Houston","ilili","Julian Street Library","Kelvin Natural Slush Co. Truck","Kessing Outdoor Pool","Lam Zhou Handmade Noodle","Land Of Plenty","Life Alive",
    "Mercedes-Benz Superdome","Nassau Street Seafood","NBA Entertainment","Olives Deli & Bakery","Pizza By Certe","Pool @ Hotel Intercontinental","Sheraton New York Times Square Hotel",
    "Silverspot Cinema","Smoothie King Center","Smorgasburg","The Westin Beijing Financial Street","The Westin New York at Times Square","UCLA Sunset Canyon Recreation Center"] 

    ##get lat longs for often freq places
    oft_lat = []
    oft_long = []
    for i in range(len(often_frequented)):
        often_frequented_place = often_frequented[i]
        lat1, long1 = find_match(longitude,latitude,places, often_frequented_place)
        oft_lat.append(lat1)
        oft_long.append(long1)

    #create dictionary for looking up most city or state of most commonly visited places
    freq_dict = {}
    #oft_lat_long = zip(oft_lat, oft_long)  #create tuple of lat longs
    for i in range(len(oft_long)):
        freq_dict[often_frequented[i]] = getplace(oft_lat[i], oft_long[i])
        print "Got freq place number " + often_frequented_place[i]
        sleep(1)

    cities = []
    states = []
    #names = fsq_data.columns.values
    #lat_lon = zip(latitude, longitude)

    for i in range(len(latitude)):
    #for i in range(100):
        if places[i] in often_frequented:
            cities.append(freq_dict[places[i]][0])  #use dictionary and look up when possible
            states.append(freq_dict[places[i]][1])
            print "repeat"
        else:
            lat = latitude[i]
            lon = longitude[i]
            city, state = getplace(latitude[i], longitude[i])
            cities.append(city)
            states.append(state)
            print str(i) + " " + places[i] 
            sleep(1)
    
    fsq_data["city"] = cities
    fsq_data["state"] = states
    filename = "FOURSQUARE_DATA_With_Local_TimesAndCity.csv"
    fsq_data.to_csv(filename,sep = ',')
    print "Done!"
    os.system('say "DunDunDun Donnne"')

if __name__ == '__main__':
    main()
