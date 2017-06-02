#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.mime.text import MIMEText
# -------------------------------------------------------------- #


__name__ = "A custom email wrapper to handle email content and custom server connection."

class EmailHandler :

	server 	= None
	mail 	= None
	
	def __init__ (self, options={}, verbose=False, log=None) :
		'''Initialize the class to handle compiling email content and sending mail objects.
		
		kwargs dictionary should include:
		--
		:param str subject - the subject to be applied to the mail object
		:param str sender_name - the section of the sender address to be resolved to a user name by most email clients. E.g. John Smith
		:param str sender_addr - the address section of the sender email john.smith@domain.com
		:param list recipients - list with elements containing a recipient name and <address>. E.g. John Doe <john.doe@domain.com>
		:param str template_file - [optional] the template file to be loaded for the message content
		:param str template_body - [optional] the raw html content to be loaded for the message content
		:param str host - [optional] if a different host should be explicitly defined
		:param int port - [optional] if a different port should be explicitly defined
		:param str title - the title of the email body
		:param list files - list with elements containing string of file paths to include for attachments to the email
		:param str exception - [optional] the python exception to display in the email body (useful in exception handling emails)
		:param str directory - [optional] the directory where any final output files may be located
		:param str filename - [optional] the filename of the file being executed at the time the EmailHandler class was called
		'''
		
		self.verbose	= verbose
		self.log		= log
		
		self.defaults 	= {
								'host' 			: None,
								'port' 			: None,
								'title'			: None,
								'exception'		: None,
								'directory'		: None,
								'filename'		: None,
								'subject'		: None,
								'sender_name' 	: None,
								'sender_addr'	: None,
								'recipients'	: None,
								'template_body' : None,
								'template_file' : None,
								'files'			: None
							}
		
		# override any existing defaults with the passed parameters
		self.defaults.update( options )
		
		# execute all the connection, content, and closing methods to execute the entire class once instantiated
		self.content()
		if self.defaults['files']:
			self.attach()
		self.connect()
		self.send()
		self.close()
		
		
	def replace (self, c) :
		'''Make any content replacements to the template file or the template body html'''
		
		if self.defaults['title'] :
			c = c.replace("{{{title}}}", self.defaults['title'])
		
		if self.defaults['exception'] :
			c = c.replace("{{{exception block}}}", self.defaults['exception'])
		
		if self.defaults['filename'] :
			c = c.replace("{{{filename}}}", self.defaults['filename'])
		
		if self.defaults['directory'] :
			c = c.replace("{{{directory}}}", self.defaults['directory'])
		
		return c
		
	
	def content (self) :
		'''Establish the mail object content using either a loaded template file or raw html'''
		
		# establish the mail object
		mail = MIMEMultipart()
		
		# add header information to the mail object
		mail['Subject'] 	= Header(self.defaults['subject'], 'utf-8')
		mail['From'] 		= "\"%s\" <%s>" % ( Header(self.defaults['sender_name'], 'utf-8'), self.defaults['sender_addr'] )
		mail['To'] 		= ", ".join( "%s" % Header( e ) for e in self.defaults['recipients'] )
		
		
		# get the mail content
		# check if a template file exists
		if self.defaults['template_file'] :
			if self.verbose :		
				m =  "STMP USING EMAIL TEMPLATE FILE %s." % self.defaults['template_file']
					
				if self.log :
					self.log.info ( m )
				else :
					print m
					
			# open the template file if one is passed to the instantiated instance
			with open(self.defaults['template_file'], 'r') as content_file :
				c = content_file.read()
		
		# if template_file is not found, a template_body (raw html) should be passed
		elif self.defaults['template_body'] :
			c = self.defaults['template_body']
		
		# call the content replacement method to substitute passed arguments into the email content html
		c = self.replace( c )
		
		# attach the mail content as an html message
		mail.attach( MIMEText(c, 'html') )
		
		self.mail = mail
	
	def attach (self):
		'''Attach the specified file set to the email'''
		
		for f in self.defaults['files'] or []:
			if f:
				with open(f, "rb") as fil:
					if self.verbose :
						m = "SMTP ATTACHING FILE TO EMAIL OBJECT %s." % f 
						
						if self.log :
							self.log.info ( m )
						else :
							print m
					
					attachment = MIMEApplication(fil.read())
					attachment.add_header('Content-Disposition','attachment', filename="%s" % os.path.basename(f))
					self.mail.attach(attachment)
	
	
	def connect (self) :
		'''Establish a connection to the smtp server using the host & port variables'''
		
		# establish the smtp connection to the server
		self.server = smtplib.SMTP( self.defaults['host'], self.defaults['port'] )
		
		if self.verbose :
			m = "CONNECTED TO SMTP SERVER %s:%s." % (self.defaults['host'], self.defaults['port'])
			
			if self.log :
				self.log.info ( m )
			else :
				print m
		
	
	def send ( self ) :
		'''Establish mail connection and send message content and header using passed parameters'''

		# pass the mail object to the smtp server
		self.server.sendmail( self.defaults['sender_addr'], self.defaults['recipients'], self.mail.as_string() )
		
		if self.verbose :
			m = "SUCCESSFULLY SENT EMAIL THROUGH SMTP SERVER OBJECT %s." % self.server
			
			if self.log :
				self.log.info ( m )
			else :
				print m

	def close (self) :
		'''Close the smtp server connection object'''
		
		# close the server connection
		self.server.close()
		
		if self.verbose :
			m = "DESTROYED SMTP CONNECTION TO %s." % self.server
						
			if self.log :
				self.log.info ( m )
			else :
				print m
		
		