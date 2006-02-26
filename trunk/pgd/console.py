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


from components import PGDSlaveDelegate

import vte
import gtk
import gobject
from Queue import Queue
from winpdb.rpdb2 import CConsole

class Terminal(PGDSlaveDelegate):

    def create_toplevel_widget(self):
        t = self.add_widget('terminal', vte.Terminal())
        t.set_size_request(0, 0)
        self._readbuf = ''
        self.print_prompt()
        return t

    def print_prompt(self):
        self.feed('')

    def feed(self, text):
        text = text.replace('\n', '\r\n')
        def _f(text):
            self.terminal.feed(text)
        gobject.idle_add(_f, text)


class InputTerminal(Terminal):

    def create_toplevel_widget(self):
        t = gtk.VBox()
        t.pack_start(super(InputTerminal, self).create_toplevel_widget())
        return t

    def on_terminal__commit(self, term, text, length):
        self._readbuf = ''.join([self._readbuf, text])
        self.feed(text.replace('\r', '\r\n'))
        self._process_readbuf()

    def _process_readbuf(self):
        if '\r' in self._readbuf:
            lines = self._readbuf.split('\r')
            self._readbuf = lines.pop()
            for line in lines:
                self.commiter.received_line(line)
                self.print_prompt()


class Console(object):
    
    def __init__(self, app):
        self.app = app
        self.main_window = app.main_window
        self.session_manager = app.session_manager
        self._commands =Queue()
        self.console = self._create_console()
        self.delegate = self._create_view()

    def _create_console(self):
        console = CConsole(self.session_manager,
                                 stdin = self,
                                 stdout = self,
                                 fSplit = True)
        return console

    def start(self):
        print 'starting console'
        self.console.start()

    def write(self, text):
        self.feed(text)
        self.delegate.print_prompt()
    
    def feed(self, text):
        self.delegate.feed(text)
    
    def _create_view(self):
        view = InputTerminal(self.app)
        view.commiter = self
        self.main_window.attach_slave('term_holder', view)
        return view

    def received_line(self, line):
        line = line + '\n'
        self._commands.put(line)

    def readline(self):
        text = self._commands.get()
        return text

    def flush(self):
        pass
