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
from collections import Counter
import streamer

client = connect.store_analytics()
#twitter = connect.twitterconnect()

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
		
def extractkeendata_collect(collect):
	return client.extraction(collect, timeframe="this_3_hours")		
		
def extractcompdata(namelist):
	print namelist
	return client.extraction(collectionname,filters=[{"property_name":"screen_names",
		"operator":"in","property_value":namelist},{"property_name":"action",
		"operator":"eq","property_value":"User Timeline"},{"property_name":"hashtagcount",
		"operator":"gte","property_value":1}])	
	
def extractcompdata_time(namelist,time_period):
	print namelist
	listOut = client.extraction(collectionname,filters=[{"property_name":"screen_names",
		"operator":"in","property_value":namelist},{"property_name":"action",
		"operator":"eq","property_value":"User Timeline"},{"property_name":"hashtagcount",
		"operator":"gte","property_value":1}],timeframe=time_period)
	print len(listOut)	
	return 	listOut	
	
def getidretweetLists():
	return client.select_unique("Retweets",target_property="orginalId")	
	
#get list of unique id's from Keen.IO to check if we should write record
def getidList(compname):
	try:
		return client.select_unique("Retweets",target_property="orginalId", group_by="competitor",
			filters=[{"property_name":"competitor","operator": "eq","property_value": compname}])
	except Exception, e:
		print e

#print getidList("Clarabridge")		

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
	
def getTweetCountsname(keen, name):
	#copy name to temp
	temp = name
	#create counter object
	name = Counter()
			

#function to pull out Keen tweets != SandSiv and determine trending Hashtags
#based on trending by month, by week, by day
def trending_concepts():
	#first lets get out data from Keen
	complist = connect.compList()
	#print complist
	keenOut = extractcompdata(complist)
	for aggs in keenOut:
		if aggs.has_key('aggtags'):
			#turn to lower

			for tags in aggs['aggtags']:
				tags = tags.lower()
	print len(keenOut)
	print keenOut[0]['screen_names']
	print keenOut[0]['aggtags']
	comp_names =[]
	hash_tags =[]
	total = Counter()
	compTotal = Counter()
	for a in range(len(keenOut)):
		if keenOut[a].has_key('aggtags'):
			#access list and determine tweets with hashtags
			total.update(keenOut[a]['aggtags'][b].lower() for b in range(len(keenOut[a]['aggtags'])))
					
		
	#listof tuple of competitors and Collections
	collectList=[]
		
# 	#loop through competitors and build counts
	for comps in complist:
		#create counter
		temp = comps
		print temp
		temps = Counter()
		for a in range(len(keenOut)):

			if keenOut[a]['screen_names'] == comps and keenOut[a].has_key('aggtags'):
			
				temps.update(element.lower() for element in keenOut[a]['aggtags'])

		collectList.append(temps.most_common(5))

					
	grandList = zip(complist,collectList)			
	#pprint.pprint (total.most_common(10))	
	#pprint.pprint( grandList)
	return grandList
	
#function to pull out Keen tweets != SandSiv and determine trending Hashtags
#based on trending by month, by week, by day
def trending_concepts_total(time_period):
	#first lets get out data from Keen
	complist = connect.compList()
	#print complist
	keenOut = extractcompdata_time(complist,time_period)
	for aggs in keenOut:
		if aggs.has_key('hashtags'):
			#turn to lower
			for tags in aggs['hashtags']:
				tags = tags.lower()
	print len(keenOut)
	comp_names =[]
	hash_tags =[]
	total = Counter()
	compTotal = Counter()
	for a in range(len(keenOut)):
		print keenOut[a]
		if keenOut[a].has_key('hashtags'):
			#access list and determine tweets with hashtags
			total.update(keenOut[a]['hashtags'][b].lower() for b in range(len(keenOut[a]['hashtags'])))
						
	return total.most_common(5)			
	
#function to pull out Keen tweets != SandSiv and determine trending Hashtags
#based on trending by month, by week, by day
def trending_concepts_collect(collection):
	#first lets get out data from Keen
	#complist = connect.compList()
	#print complist
	tags=[]
	keenOut = extractkeendata_collect(collection)
# 	for a in range(len(keenOut)):
# 		for b in keenOut[a]['data']['entities']['hashtags']:
# 			tags.append(b['text'].lower())

	standardWords =['the','of','and','a','de','-','rt','&','by','with','i','on','at','is','we',
					'no','as','via','not','be','he','in','to','la','his','que', 'el','di','e','le',
					'les','los','who','that','just','es','all','&amp;','an','all','your','can',
					'for','you','y','del','un,','was','en','will','se','but','how','have','et',
					'my','xe0','lit','many','du','uil','se','si','#','#rt','most','un','from',
					'httpu2026','me','over','xe0','il','up','httpu2026','us' ,'w','are',
					'una','her','about','pour']
	print standardWords
	words = Counter()	
	tempList=[]
	print len(keenOut)
	for b in range(len(keenOut)):
		#get the text of tweet and append Counter obj
		itemWords = keenOut[b]['data']['text'].lower().split()
		tempList =[]
		for word in itemWords:
			if word not in standardWords:
				if word.find('#') !=-1:
					tem = word.split('#')	
					word = tem[1]
				if word.find('@')!=-1:
					tem=word.split('@')
					word=tem[1]	
					
				tempList.append(word)

		words.update(tempList)
		
	
			
	#words.update(tempList)		
	return words.most_common(50)
	print tags		
	return Counter(tags).most_common(10)	
# for c in b:
# # 				print c
# 			#print keenOut[a]['data']['entities']['hashtags'][b]
# 			#tags = keenOut[a]['data']['entities']['hashtags'][b]['text'].lower()
# 		
# 		
# # 		for aggs in keenOut[a]['data']['entities']['hashtags']:
# # 			if aggs.has_key('hashtags'):
# # 				#turn to lower
# # 				for tags in aggs['hashtags']:
# # 					tags = tags.lower()
# 	print len(keenOut)
# 	comp_names =[]
# 	hash_tags =[]
# 	total = Counter()
# 	compTotal = Counter()
# 	for a in range(len(keenOut)):
# 		#pprint.pprint(keenOut[a])
# 		
# 		total.update(keenOut[a]['data']['entities']['hashtags'][b]['text'].lower() for b in range(len(keenOut[a]['data']['entities']['hashtags'])))
# 						
# 	return total.most_common(10)		

			
# #determine trends for period x, return list
# out = trending_concepts_total("this_week")
# print out

#output list of 5 tuples
# listTag = [' #'+a[0]+ " " for a in trending_concepts_total("this_3_months")]
# print listTag

#streamer.streamTrends(['Mandela'])
trenders = trending_concepts_collect("Streamer")
print trenders



	

