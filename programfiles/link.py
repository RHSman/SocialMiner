import json, pprint
from prettytable import PrettyTable
from oauthlib import *
import connections


#Keen Access items
client = connections.store_analytics()


#keen collection to append too
keencollect = connections.keenlinkedin()


#get list of unique id's from Keen.IO to check if we should write record
def getidList(compname):
	try:
		return client.select_unique(keencollect,target_property="data.updateid", group_by="company",
			filters=[{"property_name":"competitor","operator": "eq","property_value": compname}])
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
	client.add_event(keencollect, jobskeendic)
	
	#give back the dict
	return jobskeendic
	
	

def mainUpdate(statusUpdate,name, id):

	#if both content and comment
	if statusUpdate.has_key("comment") and statusUpdate.has_key("content"):
	
		print "------------BOTH-----------------"
		#create dic for Keen insertion
		commentskeendic = ({"channel":"LinkedIn","competitor":name,"data":{"company":name,
			"id":id,"action": "content","title":statusUpdate["content"]["title"],
			"url":statusUpdate["content"]["submittedUrl"],
			"content descripion":(statusUpdate["content"]["description"] if statusUpdate["content"].has_key("description") else None),
			"comment":statusUpdate["comment"], "timestamp":statusUpdate["timestamp"],
			"updateid":statusUpdate["id"], "source":statusUpdate["source"]}})
	
	elif statusUpdate.has_key("comment") and not statusUpdate.has_key("content"):
	
		print "---------ONLY COMMENT------------"
		print statusUpdate.keys()
		#create dic for Keen insertion
		commentskeendic = ({"channel":"LinkedIn","competitor":name,"data":{"company":name,
			"id":id,"action": "content",
			"comment":statusUpdate["comment"], "timestamp":statusUpdate["timestamp"],
			"updateid":statusUpdate["id"], "source":statusUpdate["source"]}})
			
			#removed 			"title":None,"url":None,"content descripion":None,
		
	elif statusUpdate.has_key("content") and not statusUpdate.has_key("comment"):
		print "---------ONLY CONTENT------------"
		commentskeendic = ({"channel":"LinkedIn","competitor":name,"data":{"company":name,
			"id":id,"action": "content",
			"title":statusUpdate["content"]["title"],"url":statusUpdate["content"]["submittedUrl"],
			"content descripion":statusUpdate["content"]["description"],
			"timestamp":statusUpdate["timestamp"],
			"updateid":statusUpdate["id"]}})
		#removed 			"comment":None, , "source":None
		
	else:
		print "---- - - - Nothing ERROR somewhere- - - ----"	
		commentskeendic = dict({"error":"no comments or content from linkedIn"})
	
	client.add_event(keencollect, commentskeendic)
	
	#give back the dictionary
	return commentskeendic
	
	
def main():
	compname,ids = connections.link_competitorlist()
	counter=0

	#list to store returned items
	updatedList =[]

	update = False
	for compid in ids:
	# 	# Pass it in to the app...
		
		app = connections.linkedin_connect()
		#linkedin.LinkedInApplication(connections.linkedin_connect())
		updates = app.get_company_updates(compid,params={'count': 200})
		
		#get list of updateids from KeenIO to cross check
		compupdateIds = getidList(compname[counter])
		try:
			print compupdateIds[0]["result"]
		except:
			print "no entry: Creating"
			#means no entry in keen, add entry
			client.add_event(keencollect, {"channel":"LinkedIn","competitor":compname[counter],"data":None})	
			compupdateIds = getidList(compname[counter])
			print compupdateIds[0]["result"]
			
		for a in updates["values"]:
			print a["updateContent"].keys()
			if a["updateContent"].has_key("companyStatusUpdate"):
				print compupdateIds[0]["result"]
				print a["updateContent"]["companyStatusUpdate"]["share"]["id"]
				if len(compupdateIds[0]["result"]) > 0:
					
					for test in compupdateIds[0]["result"]:
						if test == a["updateContent"]["companyStatusUpdate"]["share"]["id"]:

							update = False
							break
						else:
							update = True 	
				else:
					update = True
								
				if update:
					updatedList.append(mainUpdate(a["updateContent"]["companyStatusUpdate"]["share"],compname[counter],compid))
				
					print "create item"


			
			elif a["updateContent"].has_key("companyJobUpdate"):

				print "id %r" % a["updateContent"]["companyJobUpdate"]["job"]["id"]
				if len(compupdateIds[0]["result"]) > 0:
					for tester in compupdateIds[0]["result"]:
						if tester == a["updateContent"]["companyJobUpdate"]["job"]["id"]:
							update = False
							break
						else:
							update = True	
				else:
					update = True			
				if update:

					updatedList.append(jobupdate(a["updateContent"],compname[counter],compid))
					print "create job"

		counter= counter +1

	print updatedList
	#return the updated list
	return updatedList	
	
def namedComp(compname,ids):
	
	counter=0
	print "in main"
	#list to store returned items
	updatedList =[]
	print compname
	update = False
	for compid in ids:
	# 	# Pass it in to the app...
		
		app = linkedin.LinkedInApplication(auth)
		updates = app.get_company_updates(compid,params={'count': 200})
		
		#get list of updateids from KeenIO to cross check
		compupdateIds = getidList(compname[counter])
		try:
			print compupdateIds[0]["result"]
		except:
			print "no entry: Creating"
			#means no entry in keen, add entry
			client.add_event(keencollect, {"channel":"LinkedIn","competitor":compname[counter],"data":None})	
			compupdateIds = getidList(compname[counter])
			
			print compupdateIds[0]["result"]
			
		for a in updates["values"]:
			if a["updateContent"].has_key("companyStatusUpdate"):

				for test in compupdateIds[0]["result"]:
					if test == a["updateContent"]["companyStatusUpdate"]["share"]["id"]:

						update = False
						break
					else:
						update = True 	
				if update:
					updatedList.append({"channel":"LinkedIn","competitor":compname[counter],
					"data":mainUpdate(a["updateContent"]["companyStatusUpdate"]["share"],compname[counter],compid)})
					print "create item"
				else:
					print "Duplicate item"	

			
			elif a["updateContent"].has_key("companyJobUpdate"):

				print "id %r" % a["updateContent"]["companyJobUpdate"]["job"]["id"]
				
				for tester in compupdateIds[0]["result"]:
					print "Idlist item is %s" % tester
					print "updateId is %s" % a["updateContent"]["companyJobUpdate"]["job"]["id"]
					if tester == a["updateContent"]["companyJobUpdate"]["job"]["id"]:
						update = False
						break
					else:
						update = True	
				if update:
					print " \t- - - - - - -\n "
					updatedList.append({"channel":"LinkedIn","competitor":compname[counter],
						"data":jobupdate(a["updateContent"],compname[counter],compid)})
					print "create job"
				else: 
					print "Duplicate job"	

		
		print counter
		counter= counter +1

	#return the updated list
	return updatedList	
	
def getAccountId(id):
	app = connections.linkedin_connect()
	updates = app.get_company_updates(id,params={'count': 200})		
	print updates
	

	

	

	

	
	
	

	







	

