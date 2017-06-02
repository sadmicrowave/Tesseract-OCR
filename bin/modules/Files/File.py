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
import io, os, abc
import pyocr.builders, pyocr.tesseract

from PIL import Image as PI
# -------------------------------------------------------------- #

class File (object):
	""" This Abstract Base Class allows the program to interact with file paths and file objects.  It serves
	as the file path validator, while storing the open file reference pointer as an object property
	and providing custom class wrapper methods for file I/O operations like open and close.
	
	--
	:param string 	path		- string of file path
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	"""
	
	__meta__	= abc.ABCMeta
	
	_file 		= None
	_path 		= None
	_extension 	= None
	log			= None
	reqimage	= []
	verbose		= None


	def __init__ (self, path=None, log=None, verbose=True):
		self._path 		= path
		self.log		= log
		self.verbose 	= verbose
					
	def open (self, mode='rb'):
		""" After successful file path validation, open the file to a pointer.
		"""
		# open the file, with read/binary priviledges
		self._file = open(self._path, mode) if self._path else None
	
	def close (self):
		""" Close the file pointer if the pointer exists and it is marked as currently open.
		"""
		# check if the class property file is set and the built-in file object property of "closed" is not true.
		# meaning the file pointer is still open 
		if self._file and not self._file.closed :
			self._file.close()
		
		# explicitly blank out file since the pointer has been closed
		self._file = None

	def jpeg_to_text (self):
		""" Convert the jpeg image, necessary for pyocr to work, to text.
		"""
		if self.verbose and self.log : self.log.info("Starting jpeg OCR process...")
	
		buf = []
		if self.reqimage :
			# Now we just need to run OCR over the image blobs.
			for img in self.reqimage :
				# push OCR'ed characters into a buffer array, must be list type append because OCR function outputs characters into list format
				buf.append( pyocr.tesseract.image_to_string( PI.open(io.BytesIO(img)), lang="eng", builder=pyocr.builders.TextBuilder() ) )

		# apply the characters from the OCR to the text object for class retrieval
		self._text = ' '.join(buf)
	

	@abc.abstractmethod
	def file_to_jpeg (self): pass
		
	@classmethod
	def validate_path (cls, path):
		""" Validate the file path is a valid file reference path.
		"""
		# check if the file provided exists
		return path and os.path.isfile(path)

	@classmethod
	def check_extension (cls, extension):
		return extension == cls._extension
		
	# Use the @abstractproperty decorator to specify this property must be implemented/declared within the concrete/child class
	@abc.abstractproperty
	def path (self):
		raise NotImplementedError()
	
	# Use the @abstractproperty decorator to specify this property must be implemented/declared within the concrete/child class
	@abc.abstractproperty
	def text (self):
		raise NotImplementedError()
	
	# Use the @abstractproperty decorator to specify this property must be implemented/declared within the concrete/child class
	@abc.abstractproperty
	def extension (self):
		raise NotImplementedError()

	# Use the @abstractproperty decorator to specify this property must be implemented/declared within the concrete/child class
	@abc.abstractproperty
	def file (self):
		raise NotImplementedError()




		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		




	