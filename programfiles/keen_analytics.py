"""App wil get all tweets from Keen (time dependent) and work out trending 
hashtags. 
Trending over All time, Week, Month"""


"""by competitor list, get retweeted by id's, determine their reach, 
total reach of Tweet"""

from twython import Twython, TwythonError
from keen import *
import string, json, pprint
import connections as connect
import json
# import urllib
# from datetime import timedelta
# from datetime import date
# from time import *
# import string, os, sys, subprocess, time
# from sys import argv
# from collections import Counter

client = connect.store_analytics()
twitter = connect.twitterconnect()

collectionname = connect.keentweets()
retweetcollect = connect.keenretweets()


def keenmetrics_count(collectionname,filterprop,op,value):
	return client.count(collectionname, filters=[{"property_name":filterprop,"operator": op,"property_value": value}])
	
def keenmetrics_avg(collectionname,targprop,filterprop,op,value):
	return client.average(collectionname, target_property=targprop,filters=[{"property_name":filterprop,"operator": op,"property_value": value}])
	
def keenmetrics_sum(collectionname,targprop,filterprop,op,value):
	return client.sum(collectionname, target_property=targprop, filters=[{"property_name" : filterprop,"operator" : op,"property_value" : value}])
		
def checkout():
	i = keenmetrics_sum(keenmetrics,"retweet_count","screen_names","eq","SandSIV")
	print i
	j = keenmetrics_count(keenmetrics,"screen_names","eq","SandSIV")
	print j
	retweet_rate = j/i
	print retweet_rate
	
def keenmetrics1():
	count = keenmetrics_count(collectionname,"screen_names","eq","SandSIV")
	avg = keenmetrics_avg(collectionname,"retweet_count","screen_names","eq","SandSIV")
	sum = keenmetrics_sum(collectionname,"retweet_count","screen_names","eq","SandSIV")
	print count
	print avg
	print sum
	
def extractkeendata(name):
	return client.extraction(collectionname,filters=[{"property_name":"searched_item",
		"operator":"eq","property_value":name},{"property_name":"retweet_count",
		"operator":"gt","property_value":1}])
	
def getidretweetLists():
	return client.select_unique("Retweets",target_property="orginalId")	
	
#get list of unique id's from Keen.IO to check if we should write record
def getidList(compname):
	try:
		return client.select_unique("Retweets",target_property="orginalId", group_by="competitor",
			filters=[{"property_name":"competitor","operator": "eq","property_value": compname}])
	except Exception, e:
		print e

print getidList("Clarabridge")		

def get_retweeters(name):
	try:
		keenOut = extractkeendata(name)
		
		print len(keenOut)
		print raw_input('>---')
		listIds = getidList(name)[0]['result']
		print listIds
		throttlecount = 0
		update = False
		for tweets in keenOut:
			for a in listIds:
				print "a is %s and id is %s" %(a,tweets['Id'])
				if a == tweets['Id']:
					update = False
					break
				else:
					update = True
					

			print "Update = %r" % update
			if update == True:
				print "---------In Update------------"
				#Then write out to Keen

				if throttlecount < 15:
# 		
					retweets = twitter.get_retweets(id=tweets['Id'])
	# 					throttlecount = throttlecount + 1
					for x in retweets:
	# 						#print x['retweeted_status']['user']
	# 						#write out the tweet and user details to keen to avoid the throttling issues
	# 						#determine if in Keen.IO already (by Id)
						print "retweet id is %r and original id is %r" % (x['id'],tweets['Id'])
	# 						#outList.append(dict)
						client.add_event(retweetcollect, {"orginalId":tweets['Id'],"competitor":name,"data":x})	
	 						#need to go through people and get counts
						throttlecount = throttlecount + 1
	
 				else:
					break
	
			else:
				"already in list"	
	except Exception, e:
		print e

get_retweeters("Clarabridge")		

#client.add_event(retweetcollect, {"orginalId":33,"competitor":"Clarabridge","data":None})	



