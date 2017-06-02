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

# ---------------------- IMPORT LIBRARIES ---------------------- #
import os, sys, signal

from docopt import docopt
from config import ConfigurationFactory

from bin.modules.Notify import Notify
from bin.modules.Email import EmailHandler
from bin.modules.Environment import Environment
# -------------------------------------------------------------- #


def signal_handler (signum, frame):
	raise SystemExit()

if __name__ == "__main__" :
	# Docopt will check all arguments, and exit with the Usage string if they don't pass.
	# If you simply want to pass your own modules documentation then use __doc__,
	# otherwise, you would pass another docopt-friendly usage string here.
	# You could also pass your own arguments instead of sys.argv with: docopt(__doc__, argv=[your, args])
	docopt_args = docopt(__doc__, version='Tesseract OCR 1.0.0')			
	verbosity 	= docopt_args["-v"]
	e 			= None
	notify 		= None
	
	try :
		# ------------------------ Determine the script environment settings to use ----------------------------- #
		ENV = ConfigurationFactory.get_config()
				
		# ----------------- Instantiate the environment class, passing the kwargs we defined -------------------- # 
		# Create a keyword argument dictionary holding the main params we want to use throught the program defining
		# important things like where we want the files to end, etc.
		kwargs = {	
					"name"				: 'com.sadmicrowave.tesseract'
					,"log_dir"			: os.path.join(os.path.dirname(os.path.realpath(__file__)), 'var', 'log')
					,"verbose" 			: verbosity
				 }
				 
		e = Environment(**kwargs)
		# ---------------------- Setup the signal handler for upstart SIGTERM signals --------------------------- # 	
		signal.signal(signal.SIGTERM, signal_handler)
		# ------------------------------------ Initialize PyInotify Listener ------------------------------------ # 
		notify = Notify(ENV, e.log, verbosity)
		notify.start_watcher()
		# ------------------------------------------------------------------------------------------------------- #
	
	except Exception, err :
		if e and e.log :	e.log.exception( sys.exc_info()[0] )
		if notify and notify.thread_timer : 	notify.thread_timer.cancel()
		
		raise
	
	
	except KeyboardInterrupt :
		if notify.thread_timer : 	notify.thread_timer.cancel()
		
		raise
	
	# Excecute this (finally) block all the time, unless we System Exited in the above except block
	finally :
		try:
			if notify :
				for i, watcher in notify.wm._wmd.iteritems() :
					# Check if the exception buffer has any items in it, and continue to call the EmailHandler object if so in order to send out the exception email
					if watcher.proc_fun.exceptionHandler.exceptions :
						watcher.proc_fun.exceptionHandler.compileAttachments()
						watcher.proc_fun.exceptionHandler.compileExceptionBlock()
						watcher.proc_fun.exceptionHandler.email_options.update({'host':ENV.DEFAULT_SMTP_SERVER, 'port':ENV.DEFAULT_SMTP_PORT})
						# Instantiate the EmailHandler object and execute all necessary methods within by simply auto calling the __init__ constructor
						EmailHandler(watcher.proc_fun.exceptionHandler.email_options, verbose=verbosity, log=e.log if e and e.log else None)
		# catch any exceptions if something were to happen when trying to send the exception email and print them to the screen for the calling/executing user
		except Exception :
			raise
		
		finally :
			# if the environment object variable still exists then utilize the log object variable to add an exception entry to the log, since we can't email it apparently
			if e and e.log : 	e.log.info( '*** PROGRAM EXITING. ***\n' )
	
	


#-------------- Citation & Dependencies --------------#
# https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/

