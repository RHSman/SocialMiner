import smtplib
import email
from prettytable import PrettyTable
import json
import pprint
import os
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
import mimetypes


def emailGmailSender(user,pw,fromaddr ,tolist, sub, body):
	try:
		outputJSON = json.dumps(body,sort_keys=True, indent =4)
		print outputJSON
# 		headerList=[]
# 		channelList=[]
# 		dataList =[]
# 		dataOutputs=[]
# 		#Create the Pretty tables from Body
# 		#print len(body)
# 		for c in range(len(body)):
# 			print "++++++"
# 			for b in body[c]:
# 				headerList.append(b['competitor'])
# 				#print "Competitor %s" % b['competitor']
# 				channelList.append(b['channel'])
# 				#print "Data in %s is as follows" % b['channel']	
# 				print len(b['data'])
# 				dataList.append(len(b['data']))	
# 
# 									
# 		ptable = PrettyTable(["Competitor","Channel","Text"])
# 		ptable.padding_width = 2
# 		for nrows in range(len(headerList)):
# 			ptable.add_row([headerList[nrows],channelList[nrows],dataList[nrows]])
# 
# 		p2table = PrettyTable(["Competitor","Text"])
# 		p2table.padding_width = 2
# 		for nrows in range(len(headerList)):
# 			p2table.add_row([headerList[nrows],channelList[nrows],dataList[nrows]])
# 		
# 		highlightoutput = ptable.get_string()	
		


		smtp_host = 'smtp.gmail.com'
		smtp_port = 587
		server = smtplib.SMTP()
		server.connect(smtp_host,smtp_port)
		server.ehlo()
		server.starttls()
		server.login(user,pw)

		msg = email.MIMEMultipart.MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = email.Utils.COMMASPACE.join(tolist)
		msg['Subject'] = sub  
    	
		msg.attach(MIMEText(outputJSON))
		msg.attach(MIMEText('\nsent via the awesomeness of python', 'plain'))
		server.sendmail(fromaddr,tolist,msg.as_string())
	except Exception, e:
		print "Error sending the email %r" % e 	