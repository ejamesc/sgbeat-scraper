#!/usr/bin/env python

"""Use Twitter's streaming API to grab tweets.
"""

import tweetstream
from details import USERNAME, PASSWORD

#note that coordinate pairs are long/lat not lat/long
#Singapore coordinates
#locations = ["103.61,1.22","104.01356,1.456674"]

#Johor coordinates
locations = ["103.55,1.45", "103.87,1.63"]


stream = tweetstream.FilterStream(USERNAME,PASSWORD,locations=locations)
for tweet in stream:
	print "==================="
	print tweet["text"]
	print tweet["user"]["screen_name"]
	print "(%s)" % tweet["place"]["full_name"]
