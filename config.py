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
__environment__ = "DEVELOPMENT"

# ---------------------- IMPORT LIBRARIES ---------------------- #
import os, abc
# -------------------------------------------------------------- #


class ConfigurationFactory (object):
	""" Factory class for generating the proper configuration
	based on the environment in which we are running.
	"""
	
	@staticmethod
	def get_config():
		return eval('%s()' % __environment__)


class BASE (object):
	__meta__	= abc.ABCMeta
	# ---------------------- EMAIL SETUP ---------------------- #
	DEFAULT_SMTP_SERVER  		= 'smpt.emerus.com'
	DEFAULT_SMTP_PORT			= 25









class PRODUCTION (BASE):
	# ---------------- IMPLEMENTATION SETUP ------------------- #
	MEDICAL_RECORD_INVOICE_PATH = '/home/cfarmer/Coding/com.sadmicrowave.tesseract/tests/MedicalRecordInvoice2'
	


class DEVELOPMENT (BASE):
	# ---------------- IMPLEMENTATION SETUP ------------------- #
	MEDICAL_RECORD_INVOICE_PATH = '/home/cfarmer/Coding/com.sadmicrowave.tesseract/tests/MedicalRecordInvoice'
	
	