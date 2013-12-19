import plotly
import keen_analytics as analytics
import pprint


#call the Keen top 10 tags
def topfiveTags():
	listTrends = analytics.trending_concepts() 
	print "in topFive"
	
	client =[]
	listofDicts=[]
	#list should be 10 long
 	print len(listTrends)
 	for length in range(len(listTrends)):
 		#get client name
 		#print listTrends[length][0]
 		client.append(listTrends[length][0])
 		
 	colours = ["red","yellow","blue","black","orange","green","purple"]	

 		
 	for length in range(len(listTrends)):	
 		tags = []
		counts =[]
 		for item in listTrends[length][1]:
 			#print item
 			
			tags.append(item[0])
			counts.append(item[1])
		
		listofDicts.append({'name':client[length], 'x': tags, 'y': counts, 'type':'bar',
			'marker':{'color': colours[length], 'line': {'color': colours[length], 'width': 3} } })		

 		
 	for c in listofDicts:
 		pprint.pprint(c)
 		
	api_key="hvvum2tdvx"
	username = "RHS_guy"
	py = plotly.plotly(username=username, key=api_key)
	
	layout = { 'title': 'tweet Competitors', 'autosize': False, 'width': 550, 'height': 550,
		'yaxis': {'name': 'Count of Tweets','zeroline':False}, 
		'xaxis': {'type': 'Clients','zeroline':False},
		'barmode': 'group','bargap': 0.05,'bargroupgap': 0.1, 'bardir': 'v'}
	
	response = py.plot(listofDicts,layout=layout)
	url = response['url']
	filename = response['filename']

	print filename
	print response
	
	
#call the Keen top 10 tags
def toptenTags(collect):
	
	#pass in the collection
	listTrends = analytics.trending_concepts_collect(collect) 
	print "in topTen"
	
	listofDicts=[]
	#list should be 10 long
 	print listTrends
 	#for length in range(len(listTrends)):
 		#get client name
 		#print listTrends[length][0]
 		#client.append(listTrends[length][0])
 		
 	#need to create randowm number generator	
 	colours = ["red","yellow","blue","black","orange","green","purple","pink","grey","silver"]	

 		

 	tags = [trend[0] for trend in listTrends]
 	counts = [trend[1] for trend in listTrends]
 	print tags
 	
 	for a in tags:
 		listofDicts.append({'name':tags[a], 'x': tags, 'y': counts, 'type':'bar',
 			'marker':{'color': colours[length], 'line': {'color': colours[a], 'width': 3} } })	
 	
	
  		
#  	#for c in listofDicts:
#  		#pprint.pprint(c)
#  		
# 	api_key="hvvum2tdvx"
# 	username = "RHS_guy"
# 	py = plotly.plotly(username=username, key=api_key)
# 	
# 	layout = { 'title': 'Mandela', 'autosize': False, 'width': 550, 'height': 550,
# 		'yaxis': {'name': 'Count of Tweets','zeroline':False}, 
# 		'xaxis': {'type': 'Clients','zeroline':False},
# 		'barmode': 'group','bargap': 0.05,'bargroupgap': 0.1, 'bardir': 'v'}
# 	
# 	response = py.plot(listofDicts,layout=layout)
# 	url = response['url']
# 	filename = response['filename']
# 
# 	print filename
# 	print response	
# 	
	




def plotAway(data):
	api_key="hvvum2tdvx"
	username = "RHS_guy"
	py = plotly.plotly(username=username, key=api_key)
	print py

	layout = { 'title': 'tweet Competitors', 'autosize': False, 'width': 550, 'height': 550,
		'yaxis': {'name': 'Count of Tweets','zeroline':False}, 
		'xaxis': {'type': 'Clients','zeroline':False},
		'barmode': 'group','bargap': 0.25,'bargroupgap': 0.3, 'bardir': 'v'}
		
	#'catagories': cat,'
	
	input=[]
	for a in data:
		print a.keys()
		
	
	#print input
	#response = py.plot(input,layout)
	#url = response['url']
	#filename = response['filename']

	print filename
	print response
	
toptenTags("Streamer")