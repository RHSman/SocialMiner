from twython import Twython, TwythonError
from keen import *
import string, json, pprint

#keen connections
def store_analytics(): 
	#Keen Access items
	return KeenClient(
		project_id="52737d71d97b856d7300000b",
		write_key="53241d769bc67a9926c2d39e0657849b94e39d7f1988914526981e5a2beb800847f3b479a14f35be28e2f7f067e66777e89c91f8a8d3f6e2447e4b91391c394695a330ca958b0c9b77831a2728c7b47dbd944277f08f18f5535b296fed3e4b7ec5607c00ae73edf5bb23c6d8752e500d",
		read_key="0439e47fd0e67f6ccc869670b98e284e98802f481d4d3b2f9d05af160485094f8a4ca0e955ffacafb008818a7992136f51e677aef82e08aa3c850c79a3d4af1a787b19ec2f36309e11a798bae4eb5e067b01908b0463b2ea01349aae05e0e48417295a4088c2a786af43c585bd384844"
		)
		
def keentweets():
	keentweets = "TweetCapture"
	return keentweets

def keenretweets():
	return "Retweets"	

		
#twitter connections	
def twitterconnect():
	#Twitter connections
	APP_KEY = '3Yx2VyCQbFZn1hHJLqtoSw'
	APP_SECRET = 'o8wORp80ntQ8nh18vxWLfiy0USQEXtqIxkAOleseNZo'

	twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
	ACCESS_TOKEN = twitter.obtain_access_token()
	#Connect to Twitter
	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
	return twitter
	
	