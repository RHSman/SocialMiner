import feedparser
from keen import *
import emailsender
import connections

#Keen Access items
client = client = connections.store_analytics()


#get list of unique id's from Keen.IOto compare against to avoid duplicate entries
def getidDict(compname):
	keenlistids = client.select_unique("RSS_Fead",target_property="id", group_by="companyname",
		filters=[{"property_name":"companyname","operator": "eq","property_value": compname}])	
	return keenlistids	

def main():
	RSSfeedlist = connections.rss_list()
							
	#setup loop t0 got through dictionary
	count = len(RSSfeedlist)
	counter= 0
	anyUpdates=False
	updates=[]

	for arse in RSSfeedlist:
		print arse
		idDict = getidDict(arse)
		print idDict.count("result")
		if idDict.count("result") == 0:
			client.add_event("RSS_Fead", {"id":"nowt","companyname":arse})
			idDict = getidDict(arse)


		for x in range(len(RSSfeedlist[arse])):
			feeds = feedparser.parse(RSSfeedlist[arse][x])

			for a in feeds["entries"]:		
				if a.id not in idDict[0]["result"]:
					print "in Create RSS link-----------"	
					anyUpdates = True
					dic = {"title":a.title, "summary":a.summary_detail, "updated": a.updated,
						"links":a.links,"title_detail": a.title_detail,"link":a.link, 
						"author":a.author,"id": a.id, "companyname":arse}
					updates.append({"channel":"RSS Feeds", "competitor": arse,
						"data":dic})
					client.add_event("RSS_Fead", dic)
				else:
					print "in Keen already"	
		
	return updates
	
	
	

	
	
