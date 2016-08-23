#!/usr/bin/python # -*- coding: utf-8 -*-
from unidecode import unidecode
from datetime import datetime, timedelta
import csv
import os
import pandas as pd 
import math 
import numpy as np
from timezonefinder import TimezoneFinder
#from pytz import timezone  #attempted to use, didn't work for 2.7?
#import pytz
#from tzlocal import get_localzone 
#from dateutil import tz 

####ADD TIME ZONE AND CONVERT UTC TIME TO LOCAL TIMES, ADJUST FOR DAYLIGHT SAVINGS

#function converts UTC time to local time
def convert_UTC_local_timezone(local_tz, utc, timezoneset):
	for j in range(len(timezoneset)):
		if timezoneset[j] == 'Asia/Seoul' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=9)
		elif timezoneset[j] == 'Asia/Shanghai' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=8)
		elif timezoneset[j] == 'Europe/London' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=1)
		elif timezoneset[j] == 'America/New_York' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-5)
		elif timezoneset[j] == 'America/Montreal' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-5)
		elif timezoneset[j] == 'America/Detroit' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-5)
		elif timezoneset[j] == 'America/Puerto_Rico' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-5)
		elif timezoneset[j] == 'America/Cancun' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-6)
		elif timezoneset[j] == 'America/Chicago' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-6)
		elif timezoneset[j] == 'America/Denver' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-7)
		elif timezoneset[j] == 'America/Los_Angeles' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-8)
		elif timezoneset[j] == 'America/Vancouver' and local_tz == timezoneset[j]:
			utc = utc + timedelta(hours=-8)
	return utc  #return datetime object
	
def adjust_DST(utc, local_tz):
	#fmt = '%Y-%m-%d %H:%M:%S'
	#diff DST dates by area. Asia: no DST, USA/Canada same
	#cancun changed time zones in 2015 for tourism and NO DST, but central mexico has DST
	NA = ['America/Vancouver', 'America/New_York', 'America/Montreal', 'America/Denver', 'America/Detroit', 'America/Puerto_Rico', 'America/Los_Angeles', 'America/Chicago']
	no_DST = ['Asia/Seoul', 'Asia/Shanghai', 'America/Cancun']
	weird_london = 'Europe/London'
	##canada/USA time daylight savings 
	if local_tz in NA:
		DST13start = datetime(2013,3,10,2)
		DST13end = datetime(2013,11,3,2)
		DST14start = datetime(2014,3,9,2)
		DST14end = datetime(2014,11,2,2)
		DST15start = datetime(2015,3,8,2)
		DST15end = datetime(2015,11,1,2)
		DST16start = datetime(2016,3,13,2)
		DST16end = datetime(2016,11,6,2)
		if utc.year == 2013:
			if utc > DST13start and utc < DST13end:
				utc = utc + timedelta(hours=1)
		elif utc.year == 2014:
			if utc > DST14start and utc < DST14end:
				utc = utc + timedelta(hours=1)
		elif utc.year == 2015:
			if utc > DST15start and utc < DST15end:
				utc = utc + timedelta(hours=1)
		elif utc.year == 2016:
			if utc > DST16start and utc < DST16end:
				utc = utc + timedelta(hours=1)			
	#london has diff DST dates, only in london in 2014
	elif local_tz in weird_london: 
		DST14start = datetime(2014,3,30,1)
		DST14end = datetime(2014,10,26,2)
		if utc.year == 2014:
			if utc > DST14start and utc < DST14end:
				utc = utc + timedelta(hours=1)
	elif local_tz == 'America/Cancun':  #time zone change in 2015
		DST15start = datetime(2015,2,1,2)
		##assume times after 
		#time in cancun currently 1 hour behind.  before 2015, they were 2 hours behind, further adjust if checked in before this date?  
		#unclear how/when UTC time was recorded.  Assume it was converted to UTC time then based on local time
		if utc > DST15start:
			utc = utc + timedelta(hours=-1)
	return utc

def main():
	tf = TimezoneFinder()
	datefmt = '%Y-%m-%d'
	timefmt = '%H:%M:%S'
	fsq_data = pd.read_csv("foursquaredata.csv",sep = ',')

	#time zones 
	longitudes = fsq_data["Longitude"]
	latitudes = fsq_data["Latitude"]
	places = fsq_data["Place"]
	check_in_date = fsq_data["Check in Date"]
	link = fsq_data["Link"]
	description = fsq_data["Description"]
	DoW = []
	month = []
	day = []
	year = []
	hour = []
	minute = []
	date = []
	time = []
	timezones = []
	airport = []
	gym = []
	pool = []
	office = []
	placetype = []
	# -> 2009-07-10 14:44:59.193982-04:00
	for i in range(len(longitudes)):
		timezone = tf.closest_timezone_at(lng=longitudes[i], lat=latitudes[i]).encode('utf-8')
		timezones.append(timezone)
		if "Airport" in places[i]:
			airport.append(1)			
		else:
			airport.append(0)
		if "Gym" in places[i]:
			gym.append(1)
		else:
			gym.append(0)
		if "Pool" in places[i] or "Aquatic" in places[i]:
			pool.append(1)	
		else:
			pool.append(0)
		if "NBA HQ" in places[i] or "Facebook" in places[i]:
			office.append(1)
		else:
			office.append(0)
		if "Airport" in places[i]:
			placetype.append("Airport")
		elif "Gym" in places[i]:
			placetype.append("Gym")
		elif "Pool" in places[i] or "Aquatic" in places[i]: 
			placetype.append("Pool")
		elif "NBA HQ" in places[i] or "Facebook" in places[i]:
			placetype.append("Work")
		else: 
			placetype.append("None of Above")

 	###time zones 
	timezoneset = list(set(timezones))
	check_in_date[1].split(",")
	commasplit = lambda x: x.split(", ")
	spacesplit = lambda x: x.split(" ")
	checkinsplit = check_in_date.apply(commasplit)
	#fmt = '%Y-%m-%d %H:%M:%S %Z%z'  #not python 2.7 compatabile? 

	fmt = '%Y-%m-%d %H:%M:%S'
	localtimes = []  #array of local times 
	localtimes_dates = []
	#get UTC time and convert to local time
	print "Converting UTC to Local Time"
	for i in range(len(checkinsplit)):
		if checkinsplit[i][1].endswith(" +0000"):
			checkinsplit[i][1] = checkinsplit[i][1][:-6]
		
		utc = datetime.strptime(checkinsplit[i][1], '%d %b %y %H:%M:%S')  ##get time (UTC)
		utc_as_localtime = convert_UTC_local_timezone(timezones[i], utc, timezoneset)  #datetime obj w/local time
		
		#adjust for DST - get datetime object 
		localtime_DST_adjusted = adjust_DST(utc_as_localtime, timezones[i]) 

		date = localtime_DST_adjusted.strftime(datefmt)
		time = localtime_DST_adjusted.strftime(timefmt)
		localtimes.append(time)
		localtimes_dates.append(date)

		month.append(localtime_DST_adjusted.month)
		DoW.append(localtime_DST_adjusted.weekday())  #day of week
		year.append(localtime_DST_adjusted.year)
		hour.append(localtime_DST_adjusted.hour)
		minute.append(localtime_DST_adjusted.minute)
		day.append(localtime_DST_adjusted.day)  #numerical day of month

		#local_tz = timezone(timezones[i])
		#WTF doesn't work in python 2.7? but works in python 3.2???
		#utc = local_tz.localize(utc)   
		#utc.strftime(fmt)
		#datetime.strptime('03 Mar 14 17:51:19 +0000', '%d %b %y %H:%M:%S %z')  ##get UTC time 

	foursquaredata = np.column_stack([places,check_in_date, localtimes, localtimes_dates, timezones, link, latitudes, longitudes, description, DoW, month, day, year, hour, minute, placetype, gym, airport, pool, office])  #concatenate columns 
	titles = ["Place", "Check in Date", "Local Time" , "Date","Time Zone", "Link", "Latitude", "Longitude", "Description", "Day_of_Week", "Month", "Day", "Year", "Hour", "Minute", "PlaceType", "Gym", "Airport", "Pool", "Office"]
	foursquare = pd.DataFrame(foursquaredata, columns=titles)
	'''with open(filename, "w") as f:
	    writer = csv.writer(f, delimiter=",")
	    #header of the data 
	    writer.writerow(["Place", "Check in Date", "Local Time" , "Link", "Latitude", "Longitude", "Description", "Day_of_Week", "Month", "Day", "Year", "Hour", "Minute", "PlaceType", "Gym", "Airport", "Pool", "Office"])
	    writer.writerows(foursquaredata)'''

	filename = "FOURSQUARE_DATA_With_Local_Times.csv"

	foursquare.to_csv(filename,sep = ',')
	print "Done!"
	os.system('say "DunDunDun Donnne"')

if __name__ == '__main__':
	main()	


#daylight savings 
#2013: begins at 2 am on 3/10/2013 and ends at 11/3/13 at 2 am 
#2014: begins at 2 am on 3/9/2014 and ends at 11/2/14 at 2 am 
#2015: begins at 2 am on 3/8/2015 and ends at 11/1/15 at 2 am 
#2016: (March 13-Nov 6)
##adjust date based on time zones.  -- don't adjust for asia!!