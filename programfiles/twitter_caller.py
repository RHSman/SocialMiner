from twython import Twython, TwythonError
from keen import *
import string, json, pprint
import urllib
from datetime import timedelta
from datetime import date
from time import *
import string, os, sys, subprocess, time
from sys import argv
from collections import Counter
import connections


harvest_list = ['transprovence']
#'#CXM','#CEM','#CX','#VOC','#VOC','#custserv','#custexp','MRX'
#'#CEM','#CX','#VOC','#custserv',
#'#custexp','#CXM',
#'#CEM','#CX',
user = '@RHS_Guy'
keentweets = "TweetCapture"
keenmetrics = "Twitter_Metrics"
keenhashtags = "DenormHashtags"



# #Twitter connections
# APP_KEY = '3Yx2VyCQbFZn1hHJLqtoSw'
# APP_SECRET = 'o8wORp80ntQ8nh18vxWLfiy0USQEXtqIxkAOleseNZo'
# 
# twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
# ACCESS_TOKEN = twitter.obtain_access_token()

#Connect to Twitter
# twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

#Keen Access items
client = connections.store_analytics()

twitter = connections.twitterconnect()

#get list of unique id's from Keen.IOto compare against to avoid duplicate entries
def getidList(compname):
	keenlistids = client.select_unique(keentweets,target_property="Id", group_by="screen_names",
		filters=[{"property_name":"screen_names","operator": "eq","property_value": compname}])	
	return keenlistids	
	
def getidLists():
	keenlistids = client.select_unique(keentweets,target_property="Id")	
	return keenlistids		
		
def constructtweet(timelinetweets, keencollect, callaction, item):
	#BUilds up the dictionary object
	
	tweet = timelinetweets
	#print tweet.keys()
	ids = tweet['id_str']
	texts = tweet['text']
	times = tweet['created_at'] 
	screen_names = tweet['user']['screen_name']
	retweets = tweet['retweet_count'] 
		
	favorites_count = tweet['favorite_count'] 
	hashtag_count = len(tweet['entities']['hashtags']) 

	lat = (tweet['geo']['coordinates'][0] if tweet['geo'] else None) 
	longs = (tweet['geo']['coordinates'][1] if tweet['geo'] else None)
	place = (tweet['place']['full_name'] if tweet['place'] else None)
	place_type = (tweet['place']['place_type'] if tweet['place'] else None)
	hashtags = [tags['text']for tags in tweet['entities']['hashtags']]	
	user_mentions = [user_mention['screen_name'] for user_mention in tweet['entities']['user_mentions']]
	urls = [urls['url'] for urls in tweet['entities']['urls']]	
	
	
	#Create master Dictionary
	keendic = {"Id" : ids,
		"texts": texts,
		"times": times,
		"screen_names": screen_names,
		"retweet_count": retweets,
		"favorites_count": favorites_count,
		"hashtagcount": hashtag_count,
		"hashtags":hashtags,
		"lat": lat,
		"longs": longs,
		"place": place,
		"place_type": place_type,
		"user_mentions":user_mentions,
		"urls":urls,
		"action": callaction,
		"searched_item": item,
		
		}	
	client.add_event(keencollect, keendic)	
	return keendic	

		
# def toupdateornot(tweetobject,action,screenname):
# 	#takes tweet object and checks for Id in Keen.IO
# 	print tweetobject["id_str"]
# 	try:
# 		keenList = getidList(screenname)[0]["result"]
# 	except:
# 		keenList=[]
# 		keenList.append(None)
# 		
# 	
# 	#2 scenarios: Keywords or usertimelines
# 	if action == "keywords":
# 		keywordid = tweetobject['statuses']["id_str"]
# 		if keywordid in keenList:
# 			print "id %r in list" %keywordid
# 			return False
# 		else:
# 			print "------create------"
# 			return True
# 	elif action == "User Timeline":
# 		usertimeid = tweetobject["id_str"]
# 		if usertimeid in keenList:
# 			print "id %r in list" %usertimeid
# 			return False
# 			
# 		else:
# 			print "----Create----"	
# 			return True
			
			

# def keywordharvest(keywords):
# 		
# 	try:
# 		counter = 0
# 		search_results = twitter.search(q=keywords, count=50)
# 		#Get list of Id's
# 		allIds = getidLists()
# 		
# 		for a in range(len(search_results["statuses"])):
# 			if str(search_results["statuses"][a]["id"]) not in allIds:
# 				print search_results["statuses"][a]["id"]
# 				#Build dictionary
# 				constructtweet(search_results["statuses"][a],keentweets,"keywords",keywords)
# 				counter = counter +1
# 			else:
# 				print "tweet exists"
# 
# 		print "Done for keyword: %s" % keywords 	
# 		
# 		return counter
# 	
# 	except TwythonError as e:
# 	
# 		print e
			
# def hastagaggregate(tweet):
# 	try:
# 		#get tag count and screen name
# 		tagcount = len(tweet['entities']['hashtags'])
# 		
# 		#print "tagcoung %d" % tagcount
# 		screen_name = tweet['user']['screen_name']
# 		#print "screen_name %s" % screen_name
# 		j=0
# 		hashtags = []
# 		#print "in aggregate with %s" % tweet['text']
# 		#get tags in list
# 		while j < tagcount:
# 			#print j
# 			hashtags.extend([tweet['entities']['hashtags'][j]['text']])
# 			#create dictionary for Keen
# 			keendic = {"Id": tweet['id_str'],
# 				"ScreenName": screen_name, 
# 				"hashtags": tweet['entities']['hashtags'][j]['text']
# 					}
# 			#client.add_event(keenhashtags, keendic)
# 
# 			j = j+1		
# 
# 		
# 		return hashtags
# 			
# 			
# 	except TwythonError as e:
# 		
# 		print e	
			
def usertimeline(name):
	try:
		timelinetweets = twitter.get_user_timeline(screen_name=name, count=10, include_rts=0)
		#pprint.pprint(timelinetweets)
		#Get list of Id's
		validIds = getidList(name)
		print validIds
		#create return list
		updatedList =[]
		
		for a in timelinetweets:
			if len(validIds) == 0:
				#print "text is %s" % a['text']
				dict = constructtweet(a, keentweets, "User Timeline", name)
				updatedList.append({"channel":"twitter","competitor": name, "data": dict})
				
			elif a["id_str"] not in validIds[0]["result"]:
				dict = constructtweet(a, keentweets, "User Timeline", name)
				updatedList.append({"channel":"twitter","competitor": name,"data": dict})
				
		print pprint.pprint(updatedList)
		return updatedList		
		
	except TwythonError as e:
		 
		print e
		
# def tweetcounts(name,action):
# 	try:
# 		userdetails = twitter.show_user(screen_name=name)
# 		statuses_count = userdetails['statuses_count']
# 		followers_count = userdetails['followers_count']
# 		user_id = userdetails['id']
# 		friends = userdetails['friends_count']
# 		#workout retweet rate. Keen API analysis
# 		if action == "account":
# 			avgretweet = keenmetrics_avg(keentweets,"retweet_count","screen_names","eq",name)
# 			numbrecords = keenmetrics_count(keentweets,"screen_names","eq",name)
# 			retweet_sum = keenmetrics_sum(keentweets,"retweet_count","screen_names","eq",name)
# 		else:
# 
# 			avgretweet = None
# 			numbrecords = None
# 			retweet_sum = None	
# 				
# 		 
# 	#Create master Dictionary
# 		keendic = {"Id" : user_id,
# 			"total_tweets": statuses_count,
# 			"followers": followers_count,
# 			"friends": friends,
# 			"screen_names": name,
# 			"action": "User_counts",
# 			"retweet_rate": avgretweet,
# 			"total_retweets": retweet_sum }
# 		
# 		#update Keen IO
# 		#client.add_event(keenmetrics, keendic)
# 		return keendic
# 		
# 	
# 	except TwythonError as e:
# 		
# 		print e	
# 				
	
def competitors():
	try:
		#get users time line
		competitors = connections.compList()
		
		outputList = []
		print "we'll be searching and updating Keen IO with tweets from %s" % competitors
		
		for name in competitors:
			timeOutlist = usertimeline(name)
			if len(timeOutlist) > 0:
				outputList.append(timeOutlist)
			
			#tweetcounts(name,"User Timeline")
		print "FINAL - - - - -"
		print "count of List output %d" % len(outputList)

		#pprint.pprint (outputList)
		return outputList
	except Exception, e:
		print e
		
# def competitor(name):
# 	try:
# 		#get users time line
# 		#competitors = ["IMD_BSchool","INSEAD","LondonBSchool","HarvardHBS","ESADE","StanfordBiz","Columbia_Biz"]
# 		print "we'll be searching and updating Keen IO with tweets from %s" % competitors
# 		outputList = []
# 		timeOutlist = usertimeline(name)
# 		pprint.pprint(timeOutlist)
# 		if len(timeOutlist) > 0:
# 			outputList.append(timeOutlist)
# 			
# 			#tweetcounts(name,"User Timeline")
# 		print "FINAL - - - - -"
# 		print "count of List output %d" % len(outputList)
# 
# 			#pprint.pprint (outputList)
# 		return outputList
# 	except Exception, e:
# 		print e
# 	
# def whatkeywords():	
# 	#get list of keywords to search for
# 	counter = 0
# 	for name in harvest_list:
# 		print name
# 		updatescount = keywordharvest(name)
# 		counter = counter + updatescount
# 	
# 	return counter
	
competitors()	
	


	


		

	
		
	
		


                

                