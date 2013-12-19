from twython import TwythonStreamer
import json
from keen import *
import connections as connect

def streamTrends(track):

	#Twitter connections
	APP_KEY = 'kUzsLppPwR2T5QVSuxyA'
	APP_SECRET = 'DYPO6atsbiFudHKXt4jeFesVCXSmuAwVNEnAIO4eXE'

	# twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
	# ACCESS_TOKEN = twitter.obtain_access_token()
	OAUTH_TOKEN = "18134431-QcRiTLDgP7iVWFMPf1mMLUTlBQLh2LF0ASCgp73LN"
	OAUTH_TOKEN_SECRET = "n3rwM97rAqFePHeyrWLa5HIUc607iirh4pPPsGV2o4cth"



	#file to append too
	#target = open("twitter.txt", 'w')
	client = connect.store_analytics()

	class MyStreamer(TwythonStreamer):
		def on_success(self, data):

			if data.has_key('entities'):
				if len(data['entities']['hashtags']) >0:
					print data['entities']['hashtags']
					for tag in data['entities']['hashtags']:
						print tag['text']
						client.add_event("Streamer", {"action":"Trending",'tag':tag['text'],"data":data})	
# 						#which tag are we referring too?
# 						for item in track:
# 							if tag['text'] == item:
# 								print "This is the TAG!"
# 								print tag['text']
# 								searchTagger = tag['text']
# 								#client.add_event("Streamer", {"action":"Trending","tag":searchTagger,"data":data})	
# 								break;
									
			

		def on_error(self, status_code, data):
			print status_code

			# Want to stop trying to get data because of the error?
			# Uncomment the next line!
			#self.disconnect()

	stream = MyStreamer(APP_KEY, APP_SECRET,
						OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	# stream.statuses.filter(track='FrontiersIn')   
	# stream.user()   
	stream.statuses.filter(track=track, languages = ['en'])
        