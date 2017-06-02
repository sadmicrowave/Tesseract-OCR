#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import os, sys, re, glob, asyncore, pyinotify, traceback, datetime, time, threading

from FileFactory import FileFactory
from Files.File import File
from Email import EmailHandler
from Exception import ExceptionHandler
from ..implementations.Implementation import Implementation
# -------------------------------------------------------------- #

class Notify (object):
	""" This Class provides base functionality to instantiate the pyinotify
	listener on each implementation directory found within the various implementation
	types in the bin/implementations directory.
	
	--
	:param object 	ENV			- environment object containing settings constants derived by __environment__ of project
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	"""
	
	__thread_timer = None
	
	
	def __init__ (self, ENV=None, log=None, verbose=True):
		self.ENV			= ENV
		self.log 			= log
		self.verbose 		= verbose
		self.__notifiers 	= []
		self.__descriptors 	= []
		
		self.__implementation_classes = self.__import_implementations()
	
		self.__process_existing_files()
		self.__setup_watcher()
		
		self.__thread_timer	= threading.Timer(60*10, self.__process_exceptions)
		self.__thread_timer.start()
		
	
	def __import_implementations (self):
		""" This method is used to gather and import the applicable implementation files and 
		store each reference in a list for later use and iteration.
		"""
		# find all occurrences of python files within the implementations directory excluding anything beginning with '__'
		implementations = [os.path.splitext(os.path.basename(i))[0] for i in glob.glob(os.path.join( os.path.dirname(os.path.dirname(__file__)), 'implementations/[!__]*.py'))]
		assert len(implementations) > 0, 'There are no implementations found in %s' % os.path.join( os.path.dirname(os.path.dirname(__file__)), 'implementations/')

		implementation_classes = []
		for implementation in implementations:
			# import the implementation as module
			module 	= __import__('bin.implementations.%s' % implementation, fromlist=[implementation])
			# assign implementationCl to the actual module class of the imported module
			implementationCl = eval('module.%s' % implementation)
			# only use the class implementations that inherit from Implementation directly
			if implementationCl.__bases__[0] == Implementation :
				# set the implementation path accordingly to the environment path from ENV associated by the implementation class' property 'configuration_attr'
				implementationCl.implementation_path = getattr(self.ENV, implementationCl.configuration_attr)
				implementation_classes.append( implementationCl )
		
		return implementation_classes
		
		
	def __process_existing_files (self):
		""" This method is used to kick off the event process handler for files that 
		already reside within the directory, before the pyinotify listener gets instantiated.
		"""
		for implementation in self.__implementation_classes:
			existing_files = [i for i in glob.glob(os.path.join(implementation.implementation_path, '*.*')) if not re.search(' MR ', os.path.basename(i))]
			if existing_files :
				p = processEvent(implementation, self.log, self.verbose)
				for path in existing_files :
					kwargs = {  'dir'		: False
							  ,'mask'		: '0x8'
							  ,'maskname'	: 'IN_EXISTING_FILE'
							  ,'name'		: os.path.basename(path)
							  ,'path'		: implementation.implementation_path
							  ,'pathname'	: path
							  ,'wd'			: 1
							}
					event = Event(**kwargs)
					p.process_IN_CLOSE_WRITE(event)
	
	
	def __setup_watcher (self):
		""" This method will setup the pyinotify watcher for each implementation type.
		"""
		if self.__implementation_classes :
			#now we need to start the listener for the daemon, this is the whole purpose behind the app
			self.wm = pyinotify.WatchManager()
			# loop over the file paths of implementation types
			for implementation in self.__implementation_classes:
				self.__notifiers.append ( pyinotify.AsyncNotifier(self.wm, processEvent(implementation, self.log, self.verbose)) )
				self.__descriptors.append( self.wm.add_watch( implementation.implementation_path, pyinotify.IN_CLOSE_WRITE, proc_fun=processEvent(implementation, self.log, self.verbose), auto_add=True ) )
			

	def start_watcher (self):
		""" This method will start the core watcher loop to begin listening on all the registered implementation directory watchers
		created in setup_watcher.
		"""
		# only start the core loop for the watcher service if valid watchers are found in the notifiers and descriptors lists frm the setup_watcher method above
		if self.__notifiers and self.__descriptors :
			
			# this try/catch block is necessary to catch keyboard interups and explicity stop the thread_timer
			try:
				# start the core loop for all watchers
				asyncore.loop()
			except KeyboardInterrupt :
				if self.__thread_timer : self.__thread_timer.cancel()
				
					
	def __process_exceptions (self):
		""" This method is used to check periodically for any file exceptions that might have occurred during processing,
		email them as exception tracebacks and attachments, and clear the exception handler buffer to resume exception capturing.
		"""
		for i, watcher in self.wm._wmd.iteritems() :
			# Check if the exception buffer has any items in it, and continue to call the EmailHandler object if so in order to send out the exception email
			if watcher.proc_fun.exceptionHandler.exceptions :
				watcher.proc_fun.exceptionHandler.compileAttachments()
				watcher.proc_fun.exceptionHandler.compileExceptionBlock()
				watcher.proc_fun.exceptionHandler.email_options.update({'host':self.ENV.DEFAULT_SMTP_SERVER, 'port':self.ENV.DEFAULT_SMTP_PORT})
				# Instantiate the EmailHandler object and execute all necessary methods within by simply auto calling the __init__ constructor
				EmailHandler(watcher.proc_fun.exceptionHandler.email_options, verbose=self.verbose, log=self.log if self.log else None)
				# clear out the exceptions/buffer holder
				watcher.proc_fun.exceptionHandler.exceptions = []
		
	@property
	def notifiers (self):
		return self.__notifiers
	
	@property
	def descriptors (self):
		return self.__descriptors
	
	@property
	def thread_timer (self):
		return self.__thread_timer




	
	
class Event (object):
	""" This class is a pseudo-class to take a dict of kwargs and convert them to object properties to be referencable
	like event.path, etc.  It is used to simulate the event argument that pyinotify creates upon each event trigger and passes
	to it's processEvent handler.  We use this class when masking existing files/paths that are preexisting within the implementation
	directory as trigger events, to trick processEvent into handling the path the same way.
	"""
	
	def __init__ (self, **kwargs):
		# assign class variables using kwargs dict
		for name, value in kwargs.items():
			# Make each keyword-argument a property of the class.
			setattr(self, name, value)
	
	def __str__ (self):
		return "<Event dir={} mask={} maskname={} name={} path={} pathname={} wd={} >".format(self.dir, self.mask, self.maskname, self.name, self.path, self.pathname, self.wd)




class processEvent (pyinotify.ProcessEvent):
	""" This custom class inherits from pyinotify.ProcessEvent for the pyInotify listener call.
	--
	:param object	implementation - object of imported implementation class pointer for instantiation and classmethod reference if necessary
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	"""

	def __init__ (self, implementation=None, log=None, verbose=True):
		self.__implementation 		= implementation
		self.__log 					= log
		self.__verbose 				= verbose
		self.exceptionHandler 		= self.__set_exception_handler()
		self.__available_class_types = self.__get_available_types() 
	
	
	def __get_available_types (self):
		""" This method finds available file types located within bin/modules/Files, and returns
		their imported class pointer for instantiation later.
		"""
		available_class_types = []
		#event names for the pyinotify instance include the path and filename, which is important to pass to the next operation
		# get all paths to potential file type class files in the bin/modules/Files directory
		available_types = [os.path.splitext(os.path.basename(i))[0] for i in glob.glob(os.path.join( os.path.dirname(__file__), 'Files/[!__]*.py'))]
		# iterate over potential files
		for type in available_types :
			# import the file as module
			module 	= __import__('bin.modules.Files.%s' % type, fromlist=[type])
			# assign typeCl to the actual module class of the imported module
			typeCl 	= eval('module.%s' % type)
			# only use the class file type that inherit from File directly
			if typeCl.__bases__[0] == File :
				available_class_types.append( typeCl )
		
		return available_class_types


	#this may need to be edited depending on the type of file structure event that is executed when the
	def process_IN_CLOSE_WRITE (self, event):
		""" Override the built-in ProcessEvent method with custom method handling the event trigger
		in a custom way.
		"""
		try:
			# log the event
			if self.__verbose and self.__log : self.__log.info( event )
			# instantiate fileFactory to determine what the file type is and provide an implementation of the appropriate file object
			factory = FileFactory(event.pathname, self.__available_class_types, self.__log, self.__verbose)
			# instantiate the corresponding implementation based on the watcher instantiation and pass the file established from FileFactory
			i = self.__implementation(factory.file, event.path, self.__log, self.__verbose, rename_file=True)
					
		except Exception, err:
			# move the file from the implementation root path to the implementation Errors path 
			error_path = self.__implementation.move_error_file(event.pathname, event.path)
			# log the exception traceback
			self.__log.exception( sys.exc_info()[0] )
			# add the exception and new file path to the exceptionHandler for emailing
			self.exceptionHandler.add( err, error_path, traceback.format_exc() )
	
	
	def __set_exception_handler (self):		
		e = ExceptionHandler()
		e.email_options = {
						'template_file'		: '%s/assets/email/python_exception.blade.php' % os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
						,'template_body'	: None
						,'title'			: 'Tesseract %s Handler Encountered Errors' % self.__implementation.__name__
						,'sender_addr'		: 'tesseract-ocr@no-reply.emerus.com'
						,'sender_name' 		: 'Tesseract OCR Handler'
						,'recipients' 		: ["Corey Farmer <corey.farmer@emerus.com>"]
						,'subject'			: 'Tesseract %s Handler Encountered Errors!' % self.__implementation.__name__
						,'filename'			: __file__
					}
		return e
	
	@property
	def implementation (self):
		return self.__implementation.__name__
	
	
	
	
	
	
	
	
	

if __name__ == '__main__' :
	n = Notify(None, True)
	
	
	
	
	