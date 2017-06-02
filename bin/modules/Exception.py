#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import datetime, traceback, os
# -------------------------------------------------------------- #

class ExceptionHandler (object):
	""" The ExceptionHandler class is used to store found exceptions into a buffer, then at the end of the program,
	if exceptions have been found, format them into an email body and send in an exception handler type email to notify
	administrators that errors were encountered during execution.
	"""
	
	def __init__ (self) :
		# Create the instance variable buffer to hold any encountered exceptions during the program execution
		self.__buffer = []
		# Define the keyword arguments used for the EmailHandler module to format, attach any docs, and send the email to the recipients
		self.email_options = None 
	
	def add (self, e, path=None, traceback=None) :
		# Use this publically callable method to add an exception to the buffer with the appropriate properties to identify the error.
		# We want to know the error itself (e), and the traceback of the error to see the full error stack for troubleshooting (traceback).
		self.__buffer.append( {'error':e, 'path': path, 'traceback':traceback} )

	def compileAttachments (self) :
		self.email_options['files'] = [v['path'] for k,v in enumerate(self.__buffer)] or None

 	def compileExceptionBlock (self) :
 		'''Compile the body/content of the email exception message to send'''
 		# Start by creating an empty string variable to hold all exception html body components
 		exception_block = ""
 		# Iterate over each exception item that was added in the buffer
 		for exception in self.__buffer :
 			# Create an html div block which will be inserted into the html email body and styled with 
 			# CSS code found in the html email style tag.
 			exception_block += """
 							<div class='code-head'>{script}, {datetime}</div>
                             <div class='code-block'>
                                 <code>
                                 	File Path: {path}<br />
                                 	{stacktrace}
 								</code>
 							</div>
                             <br />
 						""".format(script=os.path.basename(__file__), datetime=datetime.datetime.now(), path=exception['path'], stacktrace=exception['traceback'].replace("\n","<br \>") )
 		
 		# Return the finalized string to be used and passed to the email formatting and sending module/methods
 		self.email_options['exception'] = exception_block
 
 
 	@property
 	def exceptions (self):
		return self.__buffer
	 	 
	@exceptions.setter
	def exceptions (self, value):
		self.__buffer = value