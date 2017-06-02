#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------- IMPORT LIBRARIES ---------------------- #
import unittest, os, shutil, glob, inspect

from os import sys

# add the base directory of the project to the PATH environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bin.modules.Files.PDF import PDF
from bin.modules.Files.File import File
from Notify import 
from bin.modules.FileFactory import FileFactory
from bin.implementations.Implementation import Implementation, ImplementationFactory
from bin.implementations.MedicalRecordInvoice import MedicalRecordInvoice
# -------------------------------------------------------------- #
# execution: com.sadmicrowave.tesseract$ python -m unittest discover
# execution: com.sadmicrowave.tesseract$ python -m unittest tests.test_templates.TestFunctions.test_pdf_file_convert_aubrey


class TestFunctions (unittest.TestCase):
	
	def __init__ (self, TestFunctions):
		unittest.TestCase.__init__(self, TestFunctions)
		self.available_class_types = [PDF]
		self.log	 		= None
		self.verbose 		= True
		self.imp_path 		= os.path.join(os.path.dirname(__file__), 'MedicalRecordInvoice')
		
	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_aubrey (self):		
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Aubrey_template.pdf')
		factory = FileFactory(path, [PDF], self.log, self.verbose)		
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)

		print path, iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_aurora (self):		
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Aurora_template.pdf')
		factory = FileFactory(path, [PDF], self.log, self.verbose)
		iF = ImplementationFactory(self.factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)

		print path, iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_burleson (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Burleson_template.pdf')
		factory = FileFactory(path, [PDF], self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
				
		print path, iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_cedarpark (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/CedarPark_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_colleyville (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Colleyville_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename	
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_emerusphysician (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/EmerusPhysician_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_hausman (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Hausman_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_keller (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Keller_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)
		
	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_leep (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/LEEP_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_rockwall (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Rockwall_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)

	# build test case to verify that the file conversion to jpeg process works appropriately
	def test_pdf_file_convert_schertz (self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs/Schertz_template.pdf')
		factory = FileFactory(path, self.available_class_types, self.log, self.verbose)
		iF = ImplementationFactory(factory.file, self.imp_path, [MedicalRecordInvoice], self.log, self.verbose)
		
		print iF.implementation.filename
		self.assertIsNotNone(factory.file.text)
		self.assertIsInstance(factory.file.text, basestring)
		self.assertIsInstance(iF.implementation, Implementation)
		self.assertIsInstance(iF.implementation.patient, basestring)
		self.assertIsInstance(iF.implementation.location, basestring)
		self.assertIsInstance(iF.implementation.filename, basestring)


