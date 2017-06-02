#!/bin/bash

# INSTALL AND DEPENDENCIES
display_help() {
    echo "Usage: $( basename $0 ) [option...] " >&2
    echo
    echo "   -h | --help           Display this help menu"
    echo "   -v | --verbose	       Increase logging/printing level"
    echo "   --with-db-create      Execute with database [re]creation"
    echo
    exit 1
}

OPTS=`getopt -o vh --long verbose,help -n 'test' -- "$@"`
if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi

eval set -- "$OPTS"

VERBOSE=false

while true; do
	case "$1" in
    -v | --verbose)
	    VERBOSE=true
	    shift;;
    -h | --help)
    	display_help
    	exit 0
    	;;
    -- ) shift; break;;
    * ) break;;

	esac
done


# update system registry and packages
sudo apt-get update

# ensure c++ compiler is installed
sudo apt-get install -y build-essential ghostscript libjpeg8-dev tesseract-ocr imagemagick libfreetype6 python-daemon

# get the current working directory of the INSTALL script, to be used in the pip requirements path
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# install python pip requirements
sudo pip install -r $DIR/requirements.txt

# create norad user if does not exist
if [ ! $(id -u tesseract) ]; then
  # make a new user for this specific api engine
  sudo useradd -s /bin/bash -d /var/opt/tesseract tesseract
  if $VERBOSE; then echo -e '\033[0;33m[+] Created tesseract system user.\t\033[0m'; fi
fi


# copy the upstart script to the /etc/init directory
sudo cp $DIR/tesseract-ocr.conf /etc/init/


echo -e '\033[0;33m[+] Finished. \033[0m\n'
