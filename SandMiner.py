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
KeenCollection = "TweetCapture"
KeenMetrics = "Twitter_Metrics"

#Twitter connections
APP_KEY = '****'
APP_SECRET = '****'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

#Keen Access items
client = KeenClient(
    project_id="****",
    write_key="**"
    read_key="**"
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
			
def hastagaggregate(tweet):
	try:
		#get tag count and screen name
		tagcount = len(tweet['entities']['hashtags'])
		
		#print "tagcoung %d" % tagcount
		screen_name = tweet['user']['screen_name']
		#print "screen_name %s" % screen_name
		j=0
		hashtags = []
		print "in aggregate with %s" % tweet['text']
		#get tags in list
		while j < tagcount:
			print j
			hashtags.extend([tweet['entities']['hashtags'][j]['text']])
			#create dictionary for Keen
			keendic = {"Id": tweet['id_str'],
				"ScreenName": screen_name, 
				"hashtags": tweet['entities']['hashtags'][j]['text']
					}
			client.add_event("hashtags", keendic)
			pprint.pprint(hashtags)
			j = j+1		
		#create dictionary for Keen
		
		return hashtags
			
			
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
		
# 		for tweet in timelinetweets:
# 			print "calling aggregate with %s" % tweet['text']
# 			hastagaggregate(tweet)
		aggregatedtags = [hastagaggregate(tweet) for tweet in timelinetweets]	
		pprint.pprint(aggregatedtags)	
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
				"aggtags": aggregatedtags[j],
				"lat": lat[j],
				"longs": longs[j],
				"place": place[j],
				"place_type": place_type[j],
				"url1": urls1[j],
				"url2": urls2[j],
				"mentions1": mentions1[j],
				"mentions2": mentions2[j]
				
				}

			client.add_event(KeenCollection, keendic)
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
		#workout retweet rate. Keen API analysis
		avgretweet = keenmetrics_avg(KeenCollection,"retweet_count","screen_names","eq",name)
		numbrecords = keenmetrics_count(KeenCollection,"screen_names","eq",name)
		retweet_sum = keenmetrics_sum(KeenCollection,"retweet_count","screen_names","eq",name)
		
		retweet_rate = retweet_sum//numbrecords
		print avgretweet
		print "retweet: %r" % retweet_rate
		
		print "totaltweets %d and followers %d, friends %d and retweet rate %f and sum of retweets %d (records %d)" % (statuses_count, followers_count, friends, retweet_rate, retweet_sum, numbrecords)
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
			"action": "User_counts",
			"retweet_rate": retweet_rate,
			"total_retweets": retweet_sum }
		print keendic	
		
		#update Keen IO
		client.add_event(KeenMetrics, keendic)
	
	except TwythonError as e:
		
		print e	
				
	
def competitors():
	#get users time line
	competitors = ["transprovence"]
	#competitors = ["responsetek","confirmit","Verint","clarabridge","medallia","NICE_Systems","SandSIV"]
	
	#"responsetek","confirmit","Verint","clarabridge",
	#competitors = ["IMD_BSchool","INSEAD","LondonBSchool","HarvardHBS","ESADE","StanfordBiz","Columbia_Biz"]

	print "we'll be searching and updating Keen IO with tweets from %s" % competitors
	for name in competitors:
		usertimeline(name)
		tweetcounts(name)
		
def competitor(name):
	#get users time line
	#competitors = ["IMD_BSchool","INSEAD","LondonBSchool","HarvardHBS","ESADE","StanfordBiz","Columbia_Biz"]
	print "we'll be searching and updating Keen IO with tweets from %s" % competitors
	usertimeline(name)
	tweetcounts(name)
	
def whatkeywords():	
	#get list of keywords to search for
	print "What keywords shall we sort for?"
	keyword_input = raw_input('KEywords split by comma and no space')
	keywords = keyword_input.split(',')
	#print keywords
	keywordharvest(keywords)
	
def keenmetrics_count(collectionname,filterprop,op,value):
	return client.count(collectionname, filters=[{"property_name":filterprop,"operator": op,"property_value": value}])
	
def keenmetrics_avg(collectionname,targprop,filterprop,op,value):
	return client.average(collectionname, target_property=targprop,filters=[{"property_name":filterprop,"operator": op,"property_value": value}])
	
def keenmetrics_sum(collectionname,targprop,filterprop,op,value):
	return client.sum(collectionname, target_property=targprop, filters=[{"property_name" : filterprop,"operator" : op,"property_value" : value}])
	# print sum_of_retweet
# 	total_tweets = client.count("TweetCapture",filters=[{"property_name" : "screen_names","operator" : "eq","property_value" : "SandSIV"}])
# 	print total_tweets
# 	print client.minimum("TweetCapture", target_property="hashtagcount") # => 20
# 	print client.maximum("TweetCapture", target_property="hashtagcount") # => 100
# 	print client.average("TweetCapture", target_property="hashtagcount") # => 49.2
		
def checkout():
	i = keenmetrics_sum(KeenCollection,"retweet_count","screen_names","eq","SandSIV")
	print i
	j = keenmetrics_count(KeenCollection,"screen_names","eq","SandSIV")
	print j
	retweet_rate = j/i
	print retweet_rate
	
print "What do you want to do?"
action = raw_input('> ')
if (action == "users"):
	competitors()
elif(action == "keywords"):
	whatkeywords()
elif(action=="keen"):
	print keenmetrics_count("TweetCapture","screen_names","eq","SandSIV")
	print keenmetrics_sum("TweetCapture","retweet_count","screen_names","eq","SandSIV")
	checkout()
elif(action=="account"):
	tweetcounts(raw_input('> '))
else:
	"nothing"
	#competitor(action)
	#keenmetrics()
	
	
		
	
		


                

                
