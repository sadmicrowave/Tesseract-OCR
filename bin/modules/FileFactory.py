#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import os
# -------------------------------------------------------------- #


class FileFactory (object):
	""" This is the Factory Class for the implementation of the concrete File types.  It should receive the list of available
	concrete classes to choose from and dynamically determine which concrete class to implement based on extension criteria.
	
	--
	:param string 	path 		- the path to the file to be consumed and instantiated as a concrete implementation of abstract File
	:param list		types		- list containing all the available types of concrete classes to implement based on extension matching
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	"""
	
	def __init__ (self, path=None, types=[], log=None, verbose=None):
		self.__path 	= path
		__root, self.__extension = os.path.splitext(self.__path)
		self.__types 	= types
		self.__log		= log
		self.__verbose	= verbose
		self.__file 	= self.__choose_file()
						
	def __choose_file (self):
		""" Determine which concrete File class to implement based on extension.
		"""	
		
		for concrete in self.__types :
			if concrete.check_extension(self.__extension) and concrete.validate_path(self.__path) :
				return concrete(self.__path, self.__log, self.__verbose)
	
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
	def extension (self):
		return self.__extension
		
		
	
		
