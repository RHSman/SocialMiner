#! /usr/bin/python
#Importing all the various files to call
import twitter_caller
import rss_puller
import link as linkedin
import emailsender
from timeit import default_timer

def crawlthemedia():
	start = default_timer()

	masterUpdates =[]
# 	#Let us begin
# 	#First we should call mr twitter from twitter_caller
 	masterUpdates.append(twitter_caller.competitors()) 	

# 	then lets give LinkedIn a nudge
	masterUpdates.append(linkedin.main())

 		
 	#then lets pull all the RSS feeds.
	masterUpdates.append(rss_puller.main())
 		
	#Send outputlist/dict to HTML generator for inclusion in Email

	if len(masterUpdates) > 0:
		#send somebody an email with updates
		emailsender.emailGmailSender("robert.hamiltonsmith","kate-peter1", "robert.hamiltonsmith@gmail.com",
		['rhs@sandsiv.com'], "Social Miner Updates ", masterUpdates)
	
	print default_timer() - start
	
crawlthemedia()



