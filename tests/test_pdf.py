#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import unittest, os, shutil

from os import sys

# add the base directory of the project to the PATH environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bin.modules.Files.PDF import PDF
from bin.modules.Files.File import File
from bin.modules.FileFactory import FileFactory
from bin.implementations.Implementation import Implementation, ImplementationFactory
from bin.implementations.MedicalRecordInvoice import MedicalRecordInvoice
# -------------------------------------------------------------- #
# execution: com.sadmicrowave.tesseract$ python -m unittest discover
# execution: com.sadmicrowave.tesseract$ python -m unittest tests.test_pdf.TestFunctions.test_pdf_factory


class TestFunctions (unittest.TestCase):
	
	def setUp (self):
		self.pdf_path 	 	= '/home/cfarmer/Coding/com.sadmicrowave.tesseract/tests/pdfs/Aubrey_template.pdf'
		self.pdf_mrn_path 	= '/home/cfarmer/Coding/com.sadmicrowave.tesseract/tests/pdfs/0713_001.pdf'
		self.pdf_bad_path 	= '/home/cfarmer/Coding/com.sadmicrowave.tesseract/tests/pdfs/nonexistent.pdf'
		self.imp_path 		= '/home/cfarmer/Coding/com.sadmicrowave.tesseract/tests/MedicalRecordInvoice'
		self.log	 		= None
		self.verbose 		= True
		
	# build test case to verify that the FileFactory works appropriately given good path to end file
	def test_pdf_factory (self):
		factory = FileFactory(self.pdf_path, [PDF], self.log, self.verbose)
		
		self.assertIsInstance(factory.file, PDF)


	# build test case to verify that the FileFactory works appropriately given bad path to end file
	def test_pdf_bad_factory (self):
		factory = FileFactory(self.pdf_bad_path, [PDF], self.log, self.verbose)
		
		self.assertIsNone(factory.file)
		
		
	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_visit_file_convert (self):
		factory = FileFactory(self.pdf_path, [PDF], self.log, self.verbose)
		
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)


	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_mrn_file_convert (self):
		factory = FileFactory(self.pdf_mrn_path, [PDF], self.log, self.verbose)

		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)

				
	# build test case to verify that MedicalRecordInvoice impelementation can be instantiated
	def test_visit_medical_record_invoice_implementation (self):
		factory = FileFactory(self.pdf_path, [PDF], self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
				
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)
	
	
	# build test case to verify that MedicalRecordInvoice impelementation can be instantiated
	def test_mrn_medical_record_invoice_implementation (self):
		factory = FileFactory(self.pdf_mrn_path, [PDF], self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
			
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)
		
	
	# build test case to verify error directory creation works within implementation directory
	def test_error_dir_creation (self):
		try:
			iF = ImplementationFactory(None, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
			
			raise Exception()
		except Exception :
			r = Implementation.create_error_dir(self.imp_path)
			
			self.assertTrue(os.path.exists( os.path.join(self.imp_path, '_Errors')) )
			# remove the directory so it isn't there for the next test
			shutil.rmtree( os.path.join(self.imp_path, '_Errors') )
	

if __name__ == '__main__' and __package__ is None:
	unittest.main()