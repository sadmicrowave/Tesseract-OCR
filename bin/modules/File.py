#!/usr/bin/python
# -*- coding: utf-8 -*-


__scriptname__	= "Tesseract OCR"
__author__ 		= "Corey Farmer"
__copyright__ 	= "Copyright 2017"
__credits__ 	= []
__license__ 	= "GPL"
__version__ 	= "1.0.0"
__maintainer__ 	= "Corey Farmer"
__email__ 		= "corey.farmer@emerus.com"
__status__ 		= "Development"


# ---------------------- IMPORT LIBRARIES ---------------------- #
import os

# -------------------------------------------------------------- #

class File (object):
	""" This class allows the program to interact with file paths and file objects.  It serves
	as the file path validator, while storing the open file reference pointer as an object property
	and providing custom class wrapper methods for file I/O operations like open and close.
	 
	--
	:param string path			- file path string to validate path and create a file object pointer
	:param object log			- log file object pointer for printing log info
	"""
	
	__file = None
	__path = None
	
	def __init__ (self, path=None, log=None):
		self.__path = path
		self.log 	= log
		self.validate()
	
	def validate (self):
		"""Validate the file path is a valid file reference path.
		"""
		
		# check if the file provided exists
		if not self.__path or not os.path.isfile(self.__path):
			raise Exception("The file path provided is not valid or does not exist.")

	
	def open (self):
		"""After successful file path validation, open the file to a pointer.
		"""
		
		if self.__path:
			# open the file, with read/binary priviledges
			self.__file = open(self.__path, 'rb')
	
	
	def close (self):
		"""Close the file pointer if the pointer exists and it is marked as currently open.
		"""
		
		# check if the class property file is set and the built-in file object property of "closed" is not true.
		# meaning the file pointer is still open 
		if self.__file and not self.__file.closed:
			self.__file.close()

	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def path (self):
		return self.__path
	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def file (self):
		return self.__file
