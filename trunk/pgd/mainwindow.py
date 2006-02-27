# -*- coding: utf-8 -*- 
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

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




import gtk

from kiwiviews import PythonDelegate

from icons import icons




    
class MainWindow(PythonDelegate):

    def __init__(self, parent, *args, **kw):
        self._parent = parent
        PythonDelegate.__init__(self, *args, **kw)

    def create_toplevel_widget(self):
        mw = self.add_widget('window', gtk.Window())
        mw.resize(800, 600)
        icon = icons.get(gtk.STOCK_EXECUTE)
        mw.set_icon(icon)
        vbmain = gtk.VBox(spacing=6)
        tbh = self.add_widget('toolbar_holder', gtk.EventBox())
        vbmain.pack_start(tbh, expand=False)
        mw.add(vbmain)
        hp = gtk.HPaned()
        hp.set_position(250)
        vbmain.pack_start(hp)
        vb = gtk.VBox()
        hp.pack1(vb)
        ns = self.add_widget('ns_holder', gtk.EventBox())
        vb.pack_start(ns)
        tv = self.add_widget('threads_holder', gtk.EventBox())
        vb.pack_start(tv, expand=False)
        vb2 = gtk.VPaned()
        hp.pack2(vb2)
        sv = self.add_widget('source_holder', gtk.EventBox())
        vb2.pack1(sv)
        nb = gtk.Notebook()
        vb2.pack2(nb)
        vb2.set_position(300)
        sh = self.add_widget('stack_holder', gtk.EventBox())
        nb.append_page(sh, tab_label=gtk.Label('Stack Viewer'))
        sh = self.add_widget('breaks_holder', gtk.EventBox())
        nb.append_page(sh, tab_label=gtk.Label('Breakpoints'))
        th = self.add_widget('term_holder', gtk.EventBox())
        nb.append_page(th, tab_label=gtk.Label('Command Console'))
        oh = self.add_widget('outterm_holder', gtk.EventBox())
        nb.append_page(oh, tab_label=gtk.Label('Output Console'))
        ehb = gtk.HBox(spacing=6)
        l = gtk.Label()
        l.set_markup('<big><b><tt>&gt;&gt;</tt></b></big>')
        ehb.pack_start(l, expand=False)
        ce = self.add_widget('command', gtk.Entry())
        ehb.pack_start(ce)
        vbmain.pack_start(ehb, expand=False)
        sbh = self.add_widget('statusbar_holder', gtk.EventBox())
        vbmain.pack_start(sbh, expand=False)
        return mw

    def on_window__delete_event(self, window, event):
        gtk.main_quit()

    def on_command__activate(self, entry):
        self.console.received_line(entry.get_text())
        entry.set_text('')

    def attach_slaves(self):
        self.command.grab_focus()


