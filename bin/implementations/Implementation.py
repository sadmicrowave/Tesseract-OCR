#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import os, abc
# -------------------------------------------------------------- #

class Implementation (object):
	""" This Abstract Base Class provides base functionality to extract text
	from the OCR'ed file object depending upon implementation purposes.  Each
	implementation will inherit this base class.
	
	--
	:param object	file		- file object of the instantiated file to be interacted with
	:param string	path		- path to iNotify monitored directory for implementation
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	"""
	
	__meta__	= abc.ABCMeta
	
	_path				= None
	__file				= None
	log					= None
	verbose				= None
	
	__patient_name 		= None
	__location_name		= None
	__filename			= None
	__implementation_path = None
	
	
						
	@abc.abstractmethod
	def extract_text (self): pass
	
	@abc.abstractmethod
	def create_filename (self): pass
	
	@classmethod
	def create_error_dir (cls, implementation_path):
		""" This method is used to create the error file directory within the monitored directory
		for archiving files that had errors occur during parsing operations.
		"""
		# check and make sure the error directory is there
		er = os.path.join(implementation_path, '_Errors')
		if not os.path.exists( er ):
			# make the drop directory for the outputted end result files if it does not exist
			os.makedirs( er )
			
	@classmethod
	def move_error_file (cls, path=None, implementation_path=None):
		""" This method is used to move a file from which an error occurred to the errored directory.
		"""
		if path :
			cls.create_error_dir(implementation_path)
			filename = os.path.basename(path)
			error_path = os.path.join(implementation_path, '_Errors', filename)
			os.rename(path, error_path)
			return error_path
			

	@classmethod
	def check_implementation (cls, implementation):
		return implementation == os.path.basename( os.path.normpath( cls._implementation_path ) )
	
	# Use the @abstractproperty decorator to specify this property must be implemented/declared within the concrete/child class
	@abc.abstractproperty
	def file (self):
		raise NotImplementedError()

	@file.setter
	def file (self, file):
		self.__file = file
	
	@property
	def implementation_path(self):
		return self.__implementation_path

	@implementation_path.setter
	def implementation_path (self, v):
		self.implementation_path = v











class ImplementationFactory (object):
	""" This is the Factory Class for the implementation of the concrete implementation types.  
	It should receive the list of available concrete implementation classes to choose from and 
	dynamically determine which concrete class to implement based on directory matching criteria.
	
	--
	:param object 	file		- file object from original path containing OCR'd text 
	:param string 	path 		- the path to the implementation directory that is being monitored
	:param list		types		- list containing all the available types of concrete classes to implement based on directory/path matching
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	"""
	
	def __init__ (self, file=None, path=None, types=[], log=None, verbose=None):
		self.__file		= file
		self.__path 	= path.rstrip('//').rstrip('\\') # remove any trailing path slashes
		self.__types 	= types
		self.__log		= log
		self.__verbose	= verbose
		self.__implementation 	= self.__choose_implementation()
	
	def __choose_implementation (self):
		""" Determine which concrete implementation class to implement based on directory name.
		"""
		for concrete in self.__types :
			if concrete.check_implementation( os.path.basename(os.path.normpath(self.__path)) ) :
				return concrete(self.__file, self.__path, self.__log, self.__verbose)
	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def path (self):
		return self.__path
	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def file (self):
		return self.__file
	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def implementation (self):
		return self.__implementation
	
		
	
	
	
	
	
	
	
	
	
	
	