import feedparser
from keen import *
import emailsender

#Keen Access items
client = KeenClient(
    project_id="52737d71d97b856d7300000b",
    write_key="53241d769bc67a9926c2d39e0657849b94e39d7f1988914526981e5a2beb800847f3b479a14f35be28e2f7f067e66777e89c91f8a8d3f6e2447e4b91391c394695a330ca958b0c9b77831a2728c7b47dbd944277f08f18f5535b296fed3e4b7ec5607c00ae73edf5bb23c6d8752e500d",
    read_key="0439e47fd0e67f6ccc869670b98e284e98802f481d4d3b2f9d05af160485094f8a4ca0e955ffacafb008818a7992136f51e677aef82e08aa3c850c79a3d4af1a787b19ec2f36309e11a798bae4eb5e067b01908b0463b2ea01349aae05e0e48417295a4088c2a786af43c585bd384844"
)

#get list of unique id's from Keen.IOto compare against to avoid duplicate entries
def getidDict(compname):
	keenlistids = client.select_unique("RSS_Fead",target_property="id", group_by="companyname",
		filters=[{"property_name":"companyname","operator": "eq","property_value": compname}])	
	return keenlistids	

def main():
	RSSfeedlist = {"NICE_Systems": ["http://www.nice.com/news/nrss"],
				"Verint":["http://blog.verint.com/topic/back-office-operations/rss.xml",
					"http://blog.verint.com/topic/branch-office-operations/rss.xml",
					"http://blog.verint.com/topic/contact-centers/rss.xml",
					"http://blog.verint.com/topic/EMEA-Blogs/rss.xml",
					"http://blog.verint.com/rss.xml",
					"http://blog.verint.com/topic/enterprise-intelligence/rss.xml",
					"http://blog.verint.com/topic/financial-compliance/rss.xml",
					"http://blog.verint.com/topic/marketing--customer-care/rss.xml",
					"http://blog.verint.com/topic/public-safety/rss.xml",
					"http://blog.verint.com/topic/video-management-software/rss.xml",
					"http://blog.verint.com/topic/voice-of-the-customer-analytics/rss.xml"],
				"Clarabridge":["http://loyalty360.org/feeds/resource-news"],
				"SandSIV":["http://www.customercentric.info/feed/"]
				}
							

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
	

	
	
