# -*- coding: utf-8 -*- 
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# $Id: setup.py 526 2005-08-16 18:09:12Z aafshar $

# Copyright (c) 2006 Ali Afshar

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


"""
The Python Graphical Debugger is a GTK front end to the rpdb2 debugger.
"""

import os
from setuptools import setup


try:
    import gobject
    import gtk
except ImportError:
    raise SystemExit("PDG requires PyGTK 2.8 or higher")


def discover_data_files(directory_name, extension):
    """Find data files for an extension in a data directory."""
    files = []
    for name in os.listdir(directory_name):
        if name.endswith(extension):
            files.append('%s/%s' % (directory_name, name))
    return files


setup(name="pgd",
      version="0.1",
      description="A graphical Python debugger PyGTK",
      long_description=__doc__,
      license="Expat/MIT",
      entry_points={
        'console_scripts': ["pgd = pgd.main:main"],
      },
      packages=['pgd', 'pgd.winpdb'],
      data_files = [('icons', discover_data_files('icons', 'png')),
                    ('pgd/winpdb', ['pgd/winpdb/rpdb2.py'])],
      )
