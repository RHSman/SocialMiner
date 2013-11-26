from linkedin import linkedin
import json, pprint
from prettytable import PrettyTable
from oauthlib import *
from keen import *

#KEEN access tokens
#Keen Access items
client = KeenClient(
    project_id="52737d71d97b856d7300000b",
    write_key="53241d769bc67a9926c2d39e0657849b94e39d7f1988914526981e5a2beb800847f3b479a14f35be28e2f7f067e66777e89c91f8a8d3f6e2447e4b91391c394695a330ca958b0c9b77831a2728c7b47dbd944277f08f18f5535b296fed3e4b7ec5607c00ae73edf5bb23c6d8752e500d",
    read_key="0439e47fd0e67f6ccc869670b98e284e98802f481d4d3b2f9d05af160485094f8a4ca0e955ffacafb008818a7992136f51e677aef82e08aa3c850c79a3d4af1a787b19ec2f36309e11a798bae4eb5e067b01908b0463b2ea01349aae05e0e48417295a4088c2a786af43c585bd384844"
)

#keen collection to append too
keencollect = "LinkedIn_Updates"

# Define CONSUMER_KEY, CONSUMER_SECRET,  
# USER_TOKEN, and USER_SECRET from the credentials 
# provided in your LinkedIn application

CONSUMER_KEY = '65j7nwm2nmgu'
CONSUMER_SECRET = 'j6Tcy1kDrwhb5eHU'
USER_TOKEN = 'e282ebb3-b1e6-4642-b963-8d10f3b8537d'
USER_SECRET = '4801d1d0-1798-4383-adcc-8b46d1737c3b'

RETURN_URL = '' # Not required for developer authentication

# Instantiate the developer authentication class
auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                USER_TOKEN, USER_SECRET, 
                                RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())

#get list of unique id's from Keen.IO to check if we should write record
def getidList(compname):
	try:
		return client.select_unique(keencollect,target_property="updateid", group_by="company",
			filters=[{"property_name":"company","operator": "eq","property_value": compname}])
	except Exception, e:
		print e
def jobupdate(job,name, id):

	jobskeendic = ({"channel":"LinkedIn","competitor":name,"data":{"company":name,"id":id,"action": "job", 
		"description":job["companyJobUpdate"]["job"]["description"],
		"siteJobRequest": job["companyJobUpdate"]["job"]["siteJobRequest"]["url"],
		"updateid":job["companyJobUpdate"]["job"]["id"],
		"position":job["companyJobUpdate"]["job"]["position"]["title"],
		"location":job["companyJobUpdate"]["job"]["locationDescription"]}})
	
	#put in keen
	#client.add_event(keencollect, jobskeendic)
	
	#give back the dict
	return jobskeendic
	
	

def mainUpdate(statusUpdate,name, id):

	#if both content and comment
	if statusUpdate.has_key("comment") and statusUpdate.has_key("content"):
	
		print "------------BOTH-----------------"
		#create dic for Keen insertion
		commentskeendic = dict({"company":name,"id":id,"action": "content",
			"title":statusUpdate["content"]["title"],"url":statusUpdate["content"]["submittedUrl"],
			"content descripion":(statusUpdate["content"]["description"] if statusUpdate["content"].has_key("description") else None),
			"comment":statusUpdate["comment"], "timestamp":statusUpdate["timestamp"],
			"updateid":statusUpdate["id"], "source":statusUpdate["source"]})
	
	elif statusUpdate.has_key("comment") and not statusUpdate.has_key("content"):
	
		print "---------ONLY COMMENT------------"
		print statusUpdate.keys()
		#create dic for Keen insertion
		commentskeendic = dict({"company":name,"id":id,"action": "content",
			"title":None,"url":None,
			"content descripion":None,
			"comment":statusUpdate["comment"], "timestamp":statusUpdate["timestamp"],
			"updateid":statusUpdate["id"], "source":statusUpdate["source"]})
		
	elif statusUpdate.has_key("content") and not statusUpdate.has_key("comment"):
		print "---------ONLY CONTENT------------"
		commentskeendic = dict({"company":name,"id":id,"action": "content",
			"title":statusUpdate["content"]["title"],"url":statusUpdate["content"]["submittedUrl"],
			"content descripion":statusUpdate["content"]["description"],
			"comment":None, "timestamp":statusUpdate["timestamp"],
			"updateid":statusUpdate["id"], "source":None})
		
	else:
		print "---- - - - Nothing ERROR somewhere- - - ----"	
		commentskeendic = dict({"error":"no comments or content from linkedIn"})
	
	#client.add_event(keencollect, commentskeendic)
	
	#give back the dictionary
	return commentskeendic
	
def competitorlist():
	# test id's 48781,1191295: Should turn this into a class
	name = ["Clarabridge","SandSIV Group","NICE Systems","Verint","ResponseTek",
	"Confirmit","Medallia Inc"]
	id = [48781,1191295,4728,3667,43086,10558,49697]
	return name, id
	
	
def main():
	compname,ids = competitorlist()
	counter=0
	print "in main"
	#list to store returned items
	updatedList =[]
	print compname
	for compid in ids:
	# 	# Pass it in to the app...
		
		app = linkedin.LinkedInApplication(auth)
		updates = app.get_company_updates(compid,params={'count': 200})
		
		#get list of updateids from KeenIO to cross check
		compupdateIds = getidList(compname[counter])
		print compupdateIds[0]["result"]
		
		for a in updates["values"]:
			if a["updateContent"].has_key("companyStatusUpdate"):
				print "Comp Status Update"
				print a["updateContent"]["companyStatusUpdate"]["share"]["id"] not in compupdateIds[0]["result"]
				if a["updateContent"]["companyStatusUpdate"]["share"]["id"] not in compupdateIds[0]["result"]:
					updatedList.append({"channel":"LinkedIn","competitor":compname[counter],
					"data":mainUpdate(a["updateContent"]["companyStatusUpdate"]["share"],compname[counter],compid)})
					print "create item"

			
			elif a["updateContent"].has_key("companyJobUpdate"):
				print "Job Update"
				print "id %r" % a["updateContent"]["companyJobUpdate"]["job"]["id"]
				print a["updateContent"]["companyJobUpdate"]["job"]["id"] not in compupdateIds[0]["result"]
				if a["updateContent"]["companyJobUpdate"]["job"]["id"] not in compupdateIds[0]["result"]:
					updatedList.append({"channel":"LinkedIn","competitor":compname[counter],
						"data":jobupdate(a["updateContent"],compname[counter],compid)})
					print "create job"

		
		print counter
		counter= counter +1

	#return the updated list
	return updatedList	
	







	

