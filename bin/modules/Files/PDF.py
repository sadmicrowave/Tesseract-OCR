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

from wand.image import Image
from File import File
# -------------------------------------------------------------- #

class PDF (File):
	""" This class implements the abstract class File and extends it by including methods applicable
	only to PDF document types.
	 
	--
	:param string 	path		- string of file path
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	"""
	
	# class property to be accessed by the FileFactory to type checking
	_extension = '.pdf'
	
	def __init__ (self, path=None, log=None, verbose=True):
		self._path 		= path
		self.log		= log
		self.verbose 	= verbose
		self.reqimage	= []
		self.file_to_jpeg()
		self.jpeg_to_text()
	
	def file_to_jpeg (self):
		""" Next step is to open the PDF file using wand and convert it to jpeg. Because
		the tesseract OCR module needs an image file to perform OCR on.
		"""
		
		if self._path :
			if self.verbose and self.log : self.log.info("Starting pdf conversion to jpeg process...")
		
			# Next step is to open the PDF file using wand and convert it to jpeg.
			image_jpeg = Image(filename=self._path, resolution=300).convert('jpeg')
			
			# wand has converted all the separate pages in the PDF into separate image blobs. 
			# We can loop over them and append them as a blob into the req_image list.
			for img in image_jpeg.sequence :
				self.reqimage.append( Image(image=img).make_blob('jpeg') )
				# break to stop sequencing after first blob page
				break
				
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def path (self):
		return self._path
		
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def text (self):
		return self._text
		
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def extension (self):
		return self._extension

	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def file (self):
		return self._file
	

	