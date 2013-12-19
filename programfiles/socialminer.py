#! /usr/bin/python
#Importing all the various files to call
import twitter_caller
import rss_puller
import link as linkedin
import emailsender
from timeit import default_timer
from prettytable import *
import connections

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def crawlthemedia():
	start = default_timer()

	twitterUpdates =[]
	linkedUpdates=[]
	rssUpdates=[]
# 	#Let us begin
# 	#First we should call mr twitter from twitter_caller
 	twitterUpdates.append(twitter_caller.competitors()) 	

# 	then lets give LinkedIn a nudge
	linkedUpdates.append(linkedin.main())

 		
 	#then lets pull all the RSS feeds.
	rssUpdates.append(rss_puller.main())
	
# 	"title":a.title, "summary":a.summary_detail, "updated": a.updated,
# 						"links":a.links,"title_detail": a.title_detail,"link":a.link, 
# 						"author":a.author,"id": a.id, "companyname":arse}

	z = PrettyTable(["Competitor", "Title", "Links"])
	z.align["Competitor"] = "l"
	z.align["Title"] = 'c'
	z.align["Text"] = 'c'
	z.align["Links"] = 'c'
	z.valign['Competitor'] = 't'
	z.valign['Title'] = 't'
	z.valign['Links'] = 't'
	z.padding_width = 5
	if len(rssUpdates) > 0:
		for a in range(len(rssUpdates)):
			for rss in rssUpdates[a]:
				print rss.keys()
				print rss['data'].keys()
				tempTitle=""
				tempComment=""
				tempDetail=""
				tempUrls=""
				tempDesc=""

				
				if rss['data'].has_key('title'):
					print rss['data']['title']
					chunksOut = chunks(rss['data']['title'], 40)
					for ny in chunksOut:
						tempTitle = tempTitle + "\n" + ny
						
				if rss['data'].has_key('links'):
					print rss['data']['links']
					for lk in range(len(rss['data']['links'])):
						tempUrls = tempUrls + "\n" + rss['data']['links'][lk]['href']
						
				z.add_row([rss['competitor'],tempTitle,tempUrls])
 		
	#Send outputlist/dict to HTML generator for inclusion in Email
	#loop through the updates and get simplistic data for simplistic people
	
	x = PrettyTable(["Competitor", "Text", "Links"])
	x.align["Competitor"] = "l"
	x.align["Text"] = 'c'
	x.align["Links"] = 'r'
	x.border = True
	x.header = True
	x.padding_width = 5
	
	if len(twitterUpdates) > 0:
		for a in range(len(twitterUpdates[0])):
			for update in twitterUpdates[0][a]:
			
				#take text and add /n every 30 chars:
				tempText=""
				tempUrls=""
				chunksOut = chunks(update['data']['texts'], 55)
				#print chunksOut
				for a in chunksOut:
					tempText = tempText + "\n" + a
				for b in update['data']['urls']:
					#add \n
					tempUrls = tempUrls + "\n" + b
				#print tempText	
		
				#add a row to the table
				x.add_row([update['competitor'],tempText, tempUrls])

	y = PrettyTable(["Competitor","Type", "Comment", "Content", "Desc", "Location", "Position"])
	y.align["Competitor"] = "l"
	y.align["Type"] = 'r'
	y.padding_width = 5
	if len(linkedUpdates) > 0:
		for b in range(len(linkedUpdates)):
			for links in linkedUpdates[b]:
				
				tempText=""
				tempComment=""
				tempUrls=""
				tempDesc=""
				tempPosition=""
				tempLocation=""
				
				print links['data'].keys()
				print links['data']['action']
				
				if links['data'].has_key('comment'):
					print links['data']['comment']
					chunksOut = chunks(links['data']['comment'], 55)
					for ny in chunksOut:
						tempComment = tempComment + "\n" + ny
						
				if links['data'].has_key('content description'):
					print links['data']['content description']
					chunksOut = chunks(links['data']['content description'], 40)
					for nz in chunksOut:
						tempText = tempText + "\n" + nz
				
				if links['data'].has_key('description'):
					print links['data']['description']
					chunksOut = chunks(links['data']['description'], 40)
					for nj in chunksOut:
						tempDesc = tempDesc + "\n" + nj
				
				if links['data'].has_key('position'):
					print links['data']['position']
					tempPosition = 	links['data']['position']	
				
				if links['data'].has_key('siteJobRequest'):
					print links['data']['siteJobRequest']
					
					tempUrls = 	links['data']['siteJobRequest']	
					
				if links['data'].has_key('location'):
					print links['data']['location']
					tempLocation = 	links['data']['location']		
					
						
					
				y.add_row([links['competitor'],links['data']['action'],tempComment,tempText,
					tempDesc,tempLocation,tempPosition + "\n" + tempUrls])

 	body = []
 	body.append(x)
 	body.append(y)	
 	body.append(z)
 	print z
	

	#unpack email credentials
	user,pw = connections.email_connections()
	#send somebody an email with updates
	emailsender.emailGmailSender(user,pw, user,
		connections.emailreciepients(), "Social Miner Updates ", body)
	
	print default_timer() - start
	
crawlthemedia()



