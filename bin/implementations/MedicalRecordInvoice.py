#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import os, re, importlib

from Implementation import Implementation

# import the environment constants based on status
#CONF = __import__('bin.assets.%s_CONSTANTS' % __status__, fromlist=['CONSTANTS'])
# -------------------------------------------------------------- #

class MedicalRecordInvoice (Implementation):
	""" This Class provides functionality to extract text
	from the OCR'ed File object depending upon implementation purposes.  This
	implementation is specifically designed for Medical Record Invoice parsing.
	
	--
	:param object	file		- file object of the instantiated file to be interacted with
	:param string	path		- path to iNotify monitored directory for implementation
	:param object 	log			- logging file object pointer for verbose logging purposes
	:param bool 	verbose		- verbose flag identifying if log entries should be made
	:param bool		rename_file - flag identifying if the file should be renamed, False during testing
	"""
	
	configuration_attr = 'MEDICAL_RECORD_INVOICE_PATH'
	implementation_path = None #CONF.CONSTANTS.MEDICAL_RECORD_INVOICE_PATH

	def __init__ (self, file=None, path=None, log=None, verbose=True, rename_file=False):
		self._file		= file
		self._path		= path.rstrip('//').rstrip('\\') # remove any trailing path slashes
		self.log		= log
		self.verbose 	= verbose
		
		self.extract_text()
		if rename_file :
			self.rename_file()
						

	def extract_text (self):
		self.__patient_name 	= self.__extract_patient_name()
		self.__location_name 	= self.__extract_facility_name()
		self.__filename			= self.create_filename()
				
	
	def __extract_patient_name (self, r=None):
		""" This method extracts the patient name from the appropriate location within the file.text
		attribute.
		--
		"""
		if self._file :
			#r = re.search(r'Name:\s+(.+?)(?=Visit|MRN|\d+)', self._file.text, re.I)
			r = re.search(r'Name:\s+(.+?)(?=\n)', self._file.text, re.I)
			assert r, "Patient Name could not be derived from OCR text!"
			r = r.groups()[0]
		return r or None
	
	
	def __extract_facility_name (self, r=None):
		""" This method extracts the facility name from the appropriate location within the file.text
		attribute.
		--
		"""
		if self._file :
			r = re.search(r'INVOICE:\s+(.+?)(?=\s[-|_]\s)', self._file.text, re.I)
			assert r, "Facility Name could not be derived from OCR text!"
			r = r.groups()[0]
		return r or None
	
	
	def create_filename (self):
		""" This method formats the necessary variables in a designated format for file renaming.
		"""
		assert self.__patient_name and self.__location_name, "New filename could not be determined, one or more needed arguments is empty!"
		_patient_name = self.__patient_name.split(' ')
		_patient_name.reverse()
		
		return os.path.join(os.path.dirname(self.file._path), "%s MR %s%s" % (self.__location_name, ', '.join(_patient_name).upper(), self._file.extension))
	
	def rename_file (self):
		""" This method is used to rename the file appropriately based on the new filename generated.
		"""
		assert self.__filename, "Renaming could not complete because the new filename could not be determined, one or more needed arguments is empty!"
		os.rename( self._file.path, self.__filename )
		
		if self.verbose and self.log :	self.log.info( 'File renamed from %s to %s' % (self._file.path, self.__filename))
		
			
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def file (self):
		return self._file
	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def patient (self):
		return self.__patient_name
	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def location (self):
		return self.__location_name

	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def filename (self):
		return self.__filename
			
		
		