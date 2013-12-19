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
		
		#get items from list
		
		twitterString = body[0].get_html_string() #twitter

		linkedString = body[1].get_html_string() #linkedin
		
		rssString = body[2].get_html_string() #RSS

		
		htmlBody = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
		<html lang="en">
		<head>
    	<title>Test</title>
		</head>
		<body><h1>LinkedIn Updates</h1>"""+ linkedString +"""
		<h1>Twitter Updates</h1>""" + twitterString+"""<h1>RSS Updates</h1>""" + rssString +"""</body></html>"""
		
		smtp_host = 'smtp.gmail.com'
		smtp_port = 587
		server = smtplib.SMTP()
		server.connect(smtp_host,smtp_port)
		server.ehlo()
		server.starttls()
		server.login(user,pw)


		msg = email.MIMEMultipart.MIMEMultipart('alternative')
		msg['From'] = fromaddr
		msg['To'] = email.Utils.COMMASPACE.join(tolist)
		msg['Subject'] = sub  
    	
		msg.attach(MIMEText(htmlBody, 'html','utf-8'))
		#msg.attach(MIMEText('\nsent via the awesomeness of python', 'plain'))
		server.sendmail(fromaddr,tolist,msg.as_string())
	except Exception, e:
		print "Error sending the email %r" % e 	