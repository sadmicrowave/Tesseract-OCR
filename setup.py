#!/usr/bin/python

# Copyright (C) 2017 Corey Farmer
#
# This file is part of Tesseract OCR.
#
# Hermes is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hermes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hermes.  If not, see <http://www.gnu.org/licenses/>.


from distutils.core import setup

setup(name='Tesseract OCR',
      version='1.0',
      description='Converts PDF and Images to Text via OCR',
      author='Corey Farmer',
      author_email='corey.farmer@emerus.com',
      packages=['docopt', 'pyocr', 'io', 'wand', 'atxpdf', 'python-daemon', 'pyinotify'],
     )