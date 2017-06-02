#!/bin/bash

# INSTALL NODE JS AND DEPENDENCIES
display_help() {
    echo "Usage: $( basename $0 ) [option...] " >&2
    echo
    echo "   -h | --help           Display this help menu"
    echo "   -v | --verbose	       Increase logging/printing level"
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


WD='/usr/local/include/norad'
if [ ! -d $WD ]; then
  if $VERBOSE; then echo -e '\033[0;33m[+] Initalizing git repository...\033[0m'; fi

  git clone git@gitlab.emerus.com:scripts/norad-api-repo.git $WD

  #if $VERBOSE; then echo -e '\033[0;33m[+] Initalizing git repository...\033[0m'; fi
  #git init \
  #  && git remote add origin git@gitlab.emerus.com:scripts/norad-api-repo.git \
  #  && git pull

fi
