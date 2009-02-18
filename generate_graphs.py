#!/usr/bin/env python

#This script gathers data from the NBDC and uses the google graph api
#to generate a nice graph of the last few hours of data.

import urllib2
import string

#url from the national buoy data center
#NBDC_URL = "http://www.ndbc.noaa.gov/data/hourly2/"
NBDC_URL = "http://www.ndbc.noaa.gov/data/5day2/"


# Google url for chart api
GOOGLE_CHART_API = "http://chart.apis.google.com/chart?cht=lc&&chs=250x100&chds=0,10&chl="

#default list of buoys to gather data for.  This is overidden on the
#command line.

BUOY_LIST = ['41004'] #default is edisto buoy

BUOY_DATA = {}

for buoy_id in BUOY_LIST:
    buoy_url = NBDC_URL + buoy_id + "_5day.txt"
    req = urllib2.urlopen(buoy_url)
    req_data = req.read()

    data_set = []
    for line in req_data.splitlines():
        if line.find('#') == -1:
            data = line.split()

            timeformat = "%(year)s/%(month)s/%(day)s_%(hour)s:%(minute)s" 
            time = timeformat % {'year':data[0],
                                 'month':data[1],
                                 'day':data[2],
                                 'hour':data[3],
                                 'minute':data[5]}
            if data[8] == "MM":
                data[8] = "-1"
            data_set.append(data[8])
    data_string = string.join(data_set,',')

    google_chart_url = GOOGLE_CHART_API + buoy_id + '&chd=t:'+ data_string
    print google_chart_url
    
    req0 = urllib2.urlopen(google_chart_url)
    data_file = open(buoy_id+".png",'w')

    data_file.write(req0.read())
