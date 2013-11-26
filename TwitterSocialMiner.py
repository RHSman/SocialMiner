from twython import Twython, TwythonError
from keen import *
import string, json, pprint
import urllib
from datetime import timedelta
from datetime import date
from time import *
import string, os, sys, subprocess, time
from sys import argv


harvest_list = ['SandSIV']
user = '@RHS_Guy'

#Twitter connections
APP_KEY = '3Yx2VyCQbFZn1hHJLqtoSw'
APP_SECRET = 'o8wORp80ntQ8nh18vxWLfiy0USQEXtqIxkAOleseNZo'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

#Keen Access items
client = KeenClient(
    project_id="52737d71d97b856d7300000b",
    write_key="53241d769bc67a9926c2d39e0657849b94e39d7f1988914526981e5a2beb800847f3b479a14f35be28e2f7f067e66777e89c91f8a8d3f6e2447e4b91391c394695a330ca958b0c9b77831a2728c7b47dbd944277f08f18f5535b296fed3e4b7ec5607c00ae73edf5bb23c6d8752e500d",
    read_key="0439e47fd0e67f6ccc869670b98e284e98802f481d4d3b2f9d05af160485094f8a4ca0e955ffacafb008818a7992136f51e677aef82e08aa3c850c79a3d4af1a787b19ec2f36309e11a798bae4eb5e067b01908b0463b2ea01349aae05e0e48417295a4088c2a786af43c585bd384844"
)

#Connect to Twitter
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

def keywordharvest(keywords):
	#Do action
	print keywords
	for tweet_keyword in keywords: # for each keyword, do some shit
		
		try:
			search_results = twitter.search(q=tweet_keyword, count=50)
			#search_results = twitter.get_user_timeline(screen_name="SandSIV")
			
			# print to screen
			print "---------------------RHS---------------------" 
			# print tweet.keys()
			ids = [tweet['id_str'] for tweet in search_results['statuses']]
			texts = [tweet['text'] for tweet in search_results['statuses']]
			times = [tweet['created_at'] for tweet in search_results['statuses']]
			screen_names = [tweet['user']['screen_name'] for tweet in search_results['statuses']]

			#names = [tweet['user'],['name'] for tweet in search_results['statuses']]
			# json.dumps(
			# 
			# 
			#   	
			print len(ids)
			j=0
			while j < len(ids):

				#Create master Dictionary
				keendic = {"Id" : ids[j],
					"texts": texts[j],
					"times": times[j],
					"screen_names": screen_names[j],
					"keyword_search": tweet_keyword,
					"action": "Keyword Search"}
				#print keendic	
				j= j + 1
	
				#client.add_event("RHSSandSIV", keendic)
	
			print "Done for keyword: %s" % tweet_keyword 	
		
		except TwythonError as e:
		
			print e
			
def hastagcount(tweet):
	try:
		
# 		if len(tweet['entities']['hashtags']) >= 1:
# 			print tweet['entities']['hashtags'][0]['text']
# 			hashtag_count = len(tweet['entities']['hashtags'])
# 			print "count of tags = %r" % hashtag_count
# 		else:
# 			print "no tag"	
		
		j=0
		print "tag count %d" % len(tweet['entities']['hashtags'])
		while j < len(tweet['entities']['hashtags']):
			print j
			hashtags = [tweet['entities']['hashtags'][j]['text']]
			j = j+1	
		pprint.pprint(hashtags)	
			
			
	except TwythonError as e:
		
		print e	
			
def usertimeline(name):
	try:
		timelinetweets = twitter.get_user_timeline(screen_name=name, count=200, include_rts=0)
		#search_results = twitter.get_user_timeline(screen_name="SandSIV")
		#pprint.pprint(timelinetweets)
		# print to screen
		#print "---------------------RHS---------------------" 
		
		ids = [tweet['id_str'] for tweet in timelinetweets]
		texts = [tweet['text'] for tweet in timelinetweets]
		times = [tweet['created_at'] for tweet in timelinetweets]
		screen_names = [tweet['user']['screen_name'] for tweet in timelinetweets]
		retweets = [tweet['retweet_count'] for tweet in timelinetweets]
		favorites_count = [tweet['favorite_count'] for tweet in timelinetweets]
		hashtag1 = [(tweet['entities']['hashtags'][0]['text'] if len(tweet['entities']['hashtags']) >= 1 else None) for tweet in timelinetweets]
		hashtag2 = [(tweet['entities']['hashtags'][1]['text'] if len(tweet['entities']['hashtags']) >= 2 else None) for tweet in timelinetweets]
		hashtag3 = [(tweet['entities']['hashtags'][2]['text'] if len(tweet['entities']['hashtags']) >= 3 else None) for tweet in timelinetweets]
		hashtag_count = [len(tweet['entities']['hashtags']) for tweet in timelinetweets]
# 		if hashtag_count > 0:
# 			hashtags = hastagcount(tweet)
# 		else:
# 			hashtags = ['none']
		
		lat = [(tweet['geo']['coordinates'][0] if tweet['geo'] else None) for tweet in timelinetweets]
		longs = [(tweet['geo']['coordinates'][1] if tweet['geo'] else None) for tweet in timelinetweets]
		place = [(tweet['place']['full_name'] if tweet['place'] else None) for tweet in timelinetweets]
		place_type = [(tweet['place']['place_type'] if tweet['place'] else None) for tweet in timelinetweets]
		urls1 = [(tweet['entities']['urls'][0]['expanded_url'] if len(tweet['entities']['urls']) >= 1 else None) for tweet in timelinetweets]
		urls2 = [(tweet['entities']['urls'][1]['expanded_url'] if len(tweet['entities']['urls']) >= 2 else None) for tweet in timelinetweets]
		mentions1 = [(tweet['entities']['user_mentions'][0]['screen_name'] if len(tweet['entities']['user_mentions']) >= 1 else None) for tweet in timelinetweets]
		mentions2 = [(tweet['entities']['user_mentions'][1]['screen_name'] if len(tweet['entities']['user_mentions']) >= 2 else None) for tweet in timelinetweets]
		
		#print len(ids)
		j=0
		while j < len(ids):
			print "."*j
			#Create master Dictionary
			keendic = {"Id" : ids[j],
				"texts": texts[j],
				"times": times[j],
				"screen_names": screen_names[j],
				"retweet_count": retweets[j],
				"favorites_count": favorites_count[j],
				"hashtagcount": hashtag_count[j],
				"hashtag1": hashtag1[j],
				"hashtag2": hashtag2[j],
				"hashtag3": hashtag3[j],
				"lat": lat[j],
				"longs": longs[j],
				"place": place[j],
				"place_type": place_type[j],
				"url1": urls1[j],
				"url2": urls2[j],
				"mentions1": mentions1[j],
				"mentions2": mentions2[j]
				
				}
			#print "Start: %d"% j
			print pprint.pprint(keendic)	
			#print "Stop: %d" % j
			client.add_event("Bschool_Tweets", keendic)
			j= j + 1

		

		print "Done for user: %s" % name	
		
	except TwythonError as e:
		
		print e
		
def tweetcounts(name):
	try:
		userdetails = twitter.show_user(screen_name=name)
		statuses_count = userdetails['statuses_count']
		followers_count = userdetails['followers_count']
		user_id = userdetails['id']
		friends = userdetails['friends_count']
		print "totaltweets %d and followers %d, friends %d" % (statuses_count, followers_count, friends)
		
		#workout retweet rate. Keen API analysis
		
		#Ideal would be to get scope of depth (retweeted by whom and how many followers to they have?
		#influencer rate
		#Total number tweeted too
		#Combine with click through rate of link (need correlation table)
		
		 
	#Create master Dictionary
		keendic = {"Id" : user_id,
			"total_tweets": statuses_count,
			"followers": followers_count,
			"friends": friends,
			"screen_names": name,
			"action": "User_counts"}
		print keendic	
		
		#update Keen IO
		client.add_event("BSchoolMetrics", keendic)
	
	except TwythonError as e:
		
		print e	
				
	
def competitors():
	#get users time line
	#competitors = ["responsetek","confirmit","Verint","clarabridge","medallia","NICE_Systems","SandSIV"]
	competitors = ["IMD_BSchool","INSEAD","LondonBSchool","HarvardHBS","ESADE","StanfordBiz","Columbia_Biz"]

	print "we'll be searching and updating Keen IO with tweets from %s" % competitors
	for name in competitors:
		usertimeline(name)
		tweetcounts(name)
		
def competitor(name):
	#get users time line
	#competitors = ["IMD_BSchool","INSEAD","LondonBSchool","HarvardHBS","ESADE","StanfordBiz","Columbia_Biz"]
	print "we'll be searching and updating Keen IO with tweets from %s" % competitors
	usertimeline(name)
	#tweetcounts(name)
	


def whatkeywords():	
	#get list of keywords to search for
	print "What keywords shall we sort for?"
	keyword_input = raw_input('KEywords split by comma and no space')
	keywords = keyword_input.split(',')
	#print keywords
	keywordharvest(keywords)
	
print "What do you want to do?"
action = raw_input('> ')
if (action == "users"):
	competitors()
elif(action == "keywords"):
	whatkeywords()
else:
	competitor(action)
	#hastagcount(action)
	
		
	
		


                

                