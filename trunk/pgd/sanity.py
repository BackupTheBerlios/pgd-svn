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


import os
import sys


def exit(msg, msg2='', e=None):
    sys.stderr.write('FATAL: %s\n%s\n' % (msg, msg2))
    if e is not None:
        raise e
    sys.exit(1)


try:
    import gtk
    import gobject
    gtk.threads_init()
except ImportError, e:
    msg = 'Missing Dependency: PyGTK'
    msg = ('PyGTK 2.6 is required to run pgd. '
           'Please visit http://www.pygtk.org/.')
    exit(msg, e)


def gui_exit(msg, msg2, url='', e=None):
    import hig
    d = hig.dialog_error(
            title='Python Graphical Debugger',
            primary_text=msg,
            secondary_text=('<span color="#903030"><i><b>%s</b></i></span>'
                            '\n\n%s' % (msg2, url))
        )
    exit(msg, msg2, e)


try:
    import setuptools
    del setuptools
except ImportError, e:
    msg = 'Setuptools missing'
    msg2 = 'Setuptools is required to run pgd.'
    url = 'http://peak.telecommunity.com/DevCenter/setuptools'
    gui_exit(msg, msg2, url, e)


try:
    import kiwi
    del kiwi
except ImportError, e:
    msg = 'Kiwi missing'
    msg2 = 'Kiwi is required to run pgd.'
    url = 'http://kiwi.async.br/'
    gui_exit(msg, msg2, url, e)

