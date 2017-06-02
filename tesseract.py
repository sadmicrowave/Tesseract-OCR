#!/usr/bin/python
# -*- coding: utf-8 -*-


# The following section is neccesary in order for DocOpt command line argument parsing module to operate
# Do not change the following syntax unless you are familiar with DocOpt specifications.
"""Tesseract OCR is a python daemon utility to perform Object Character Recognition (OCR) operations 
on scanned PDF document files.  Further operations, after text parsing, can be configured based on implementation. 

Usage:
	tesseract.py [-h | --help]
	tesseract.py [-v | --verbose]
	tesseract.py --version

Options:
	-h,--help	: show this help message
	-v,--verbose    : display/log more text output
	--version	: show version
"""

__scriptname__	= "Tesseract OCR"
__author__ 		= "Corey Farmer"
__copyright__ 	= "Copyright 2017"
__credits__ 	= []
__license__ 	= "GPL"
__version__ 	= "1.0.0"
__maintainer__ 	= "Corey Farmer"
__email__ 		= "corey.farmer@emerus.com"
__status__ 		= "Development"




# ----------------------- LOGIC MAPPING ------------------------ #

# 	Command Line Interface Execution
#		|
#		|-> Parse Command Line Arguments with DocOpt module
#		|-> Instantiate ExceptionHandler Class
#		|-> Instantiate Environment Class
#		|	|
#		|	|-> Create archive and file drop directories
#		|	|-> Create and setup log object
#		|-> Daemonize the script to run as a background process
#		|-> Iterate over drop directory for initial documents found, before initializing inotify listener
#		|-> Initialize inotify listener on directory for directory writes
#		|-> Email failure formatted email, if applicable
#		|-> End program



# ---------------------- IMPORT LIBRARIES ---------------------- #
import pyocr, io, os, sys, daemon, logging
import pyocr.builders, pyocr.tesseract

from docopt import docopt
from wand.image import Image
from PIL import Image as PI

from bin.modules.File import File
from bin.modules.Email import EmailHandler
from bin.modules.Environment import Environment
# -------------------------------------------------------------- #






class TesseractFactory (object):
	""" This is the main class for the OCR work.  It receives file
	objects and outputs file text to a private object property for retrieval
	from a built-in getter method.
	
	--
	:param object file			- file pointer of file to open and attempt OCR
	:param object log			- log file object pointer for printing log info
	"""
	
	__text = ''
	__file = None
	
	def __init__ (self, file=None, log=None):
		self.__file = file
		self.log	= log
		self.imageConvert()
		
	def imageConvert (self):
		""" Next step is to open the PDF file using wand and convert it to jpeg. Because
		the tesseract OCR module needs an image file to perform OCR on.
		"""
		
		if self.__file :
			self.log.info("Starting pdf conversion to jpeg process...")
			# Now we need to setup a list which will be used to hold our images.
			req_image = []
			
			# Next step is to open the PDF file using wand and convert it to jpeg.
			image_jpeg = Image(filename=self.__file, resolution=300).convert('jpeg')
			
			
			# wand has converted all the separate pages in the PDF into separate image blobs. 
			# We can loop over them and append them as a blob into the req_image list.
			for img in image_jpeg.sequence:
				req_image.append( Image(image=img).make_blob('jpeg') )
			
			self.log.info("Starting jpeg OCR process...")
			# Now we just need to run OCR over the image blobs.
			for img in req_image:
				self.__text += ( pyocr.tesseract.image_to_string( PI.open(io.BytesIO(img)), lang="eng", builder=pyocr.builders.TextBuilder() ) )
	
	# Use the @property method decorator to designate this method as a class/object property getter.
	@property
	def text (self):
		# Return text property but not before stripping out any line breaks
		return self.__text.replace('\n','')
	


class Daemonize (object):
	""" This class is a wrapper class for the daemon process of pushing this program/script
	to the background.  It allows us to add methods for certain functionality that should be 
	associated with daemonizing like killing existing/executing processes if necessary.
	
	--
	:param object log			- log file object pointer for printing log info
	"""
	
	def __init__ (self, log=None):
		self.log = log
		# check if this daemon program is already running in the background
		self.isRunning()
		
	def isRunning (self):
		""" This method verifies that an instance of this program is not already running.  
		If count of process id`s is greater than 1 close program.
		"""
		try:
			if len( os.popen( "ps -aef | grep -i 'tesseract.py' | grep -v 'grep' | awk '{ print $2 }'" ).read().strip() ) > 0:
				raise SystemExit(0)
				
		except Exception:
			self.log.exception( sys.exc_info()[0] )
			raise

	








	



class ExceptionHandler (object):
	""" The ExceptionHandler class is used to store found exceptions into a buffer, then at the end of the program,
	if exceptions have been found, format them into an email body and send in an exception handler type email to notify
	administrators that errors were encountered during execution.
	"""
	
	def __init__ (self) :
		# Create the instance variable buffer to hold any encountered exceptions during the program execution
		self.__buffer = []

	def add (self, e, traceback) :
		# Use this publically callable method to add an exception to the buffer with the appropriate properties to identify the error.
		# We want to know the error itself (e), and the traceback of the error to see the full error stack for troubleshooting (traceback).
		self.__buffer.append( {'error':e, 'traceback':traceback} )
	

 	def compileExceptionBlock (self) :
 		'''Compile the body/content of the email exception message to send'''
 		# Start by creating an empty string variable to hold all exception html body components
 		exception_block = ""
 		# Iterate over each exception item that was added in the buffer
 		for exception in self.__buffer :
 			# Create an html div block which will be inserted into the html email body and styled with 
 			# CSS code found in the html email style tag.
 			exception_block += """
 							<div class='code-head'>{script}, {datetime}</div>
                             <div class='code-block'>
                                 <code>
                                 	{stacktrace}
 								</code>
 							</div>
                             <br />
 						""".format(script=os.path.basename(__file__), datetime=datetime.datetime.now(), stacktrace=exception['traceback'].replace("\n","<br \>") )
 		
 		# Return the finalized string to be used and passed to the email formatting and sending module/methods
 		return exception_block




if __name__ == "__main__":
	# Docopt will check all arguments, and exit with the Usage string if they don't pass.
	# If you simply want to pass your own modules documentation then use __doc__,
	# otherwise, you would pass another docopt-friendly usage string here.
	# You could also pass your own arguments instead of sys.argv with: docopt(__doc__, argv=[your, args])
	docopt_args = docopt(__doc__, version='Tesseract OCR 1.0.0')			
	verbosity 	= docopt_args["-v"]
	
	
	sample_file = "%s/bin/samples/WESTOVER MR MORALES, RUBEN.pdf" % os.path.dirname(os.path.realpath(__file__))
	
	try :
		# Instantiate the ExceptionHandler object instance in order to add exceptions to the buffer for emailing later
		exceptionHandler = ExceptionHandler()
		
		# ----------------- Instantiate the environment class, passing the kwargs we defined -------------------- # 
		# Create a keyword argument dictionary holding the main params we want to use throught the program defining
		# important things like where we want the files to end, etc.
		kwargs = {	
					"name"				: 'com.sadmicrowave.tesseract'
					,"drop_dir"			: '%s/var/tmp' % os.path.dirname(os.path.realpath(sys.argv[0]))
					,"archive_dir" 		: "%s/var/archive" % os.path.dirname(os.path.realpath(sys.argv[0]))
					,"log_dir"			: "%s/var/log" % os.path.dirname(os.path.realpath(sys.argv[0]))
					,"verbose" 			: verbosity
				 }

		e = Environment(**kwargs)
		# Set the new directory structures, from within the Environment class instantiation
		e.setupEnvironment_()

		# ---------------------- Daemonize the script by splitting the process id twice ------------------------- # 
		d = Daemonize(e.log)
		# Daemonization must occurr in root/main and not in an instantiated class
		context = daemon.DaemonContext( files_preserve = [e.log.handlers[0].stream,], )
		context.open()
					
		# ------------------------ Initialize PyInotify Listener for Drop Directory ----------------------------- # 
		
		
		# ------------------------------------------------------------------------------------------------------- #
		
		
		file = File(sample_file, e.log)	
		t =	TesseractFactory(file.path, e.log)
		print t.text
		
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	except Exception :
		if e and e.log:
			e.log.exception( sys.exc_info()[0] )
			
		raise
		 
	finally :
		if e and e.log :
			e.log.info( "***PROGRAM EXITING.***" )




#-------------- Citation & Dependencies --------------#
# https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/

