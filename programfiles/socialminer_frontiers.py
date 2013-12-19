#! /usr/bin/python
#Importing all the various files to call
import twitter_caller
import rss_puller
import link as linkedin
import emailsender
from timeit import default_timer


def complinkList():
	# test id's 48781,1191295: Should turn this into a class
	name = ["LinkedIn"]
	id = [48781]

	return name, id

def comptwitterList():
	name = "FrontiersIn"
	return name	

def crawlthemedia():
	start = default_timer()

	masterUpdates =[]
# 	#Let us begin
# 	#First we should call mr twitter from twitter_caller
	name = comptwitterList()
 	masterUpdates.append(twitter_caller.competitor(name)) 	

# 	then lets give LinkedIn a nudge
	#comp,ids = complinkList()
	#masterUpdates.append(linkedin.namedComp(comp,ids))

 		
 	#then lets pull all the RSS feeds.
	#masterUpdates.append(rss_puller.main())
 		
	#Send outputlist/dict to HTML generator for inclusion in Email

	print len(masterUpdates)
	if len(masterUpdates) > 1:
		print "Emailing . . . . . "
 		#send somebody an email with updates
 		emailsender.emailGmailSender("robert.hamiltonsmith","kate-peter1", "robert.hamiltonsmith@gmail.com",
 		['robert.hamiltonsmith@gmail.com'], "Social Miner Updates ", masterUpdates)

	print default_timer() - start
	
crawlthemedia()



