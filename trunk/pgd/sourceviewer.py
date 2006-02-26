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


import gtk
import gobject

from components import PGDSlaveDelegate

from pida.utils.culebra import edit
from icons import icons

class Culebra(edit.CulebraView):

    def __init__(self, parent):
        edit.gtksourceview.SourceView.__init__(self)
        self.cb = parent
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.on_bp_event)
        self.set_auto_indent(True)
        self.set_show_line_numbers(True)
        self.set_show_line_markers(True)
        self.set_tabs_width(4)
        self.set_margin(80)
        self.set_show_margin(True)
        self.set_smart_home_end(True)
        self.set_highlight_current_line(True)
        self.set_insert_spaces_instead_of_tabs(True)
        self.set_marker_pixbuf('bp', icons.get(gtk.STOCK_STOP))
        self.set_font('Monospace 9')
        
        #self.search_bar = SearchBar(self, action_group)
        #self.replace_bar = ReplaceBar(self, self.search_bar, action_group)
        #self.set_action_group(action_group)
        edit.make_source_view_indentable(self)

    def on_bp_event(self, view, event):
        buf = self.get_buffer()
        if event.window is self.get_window(gtk.TEXT_WINDOW_LEFT):
            bc = self.window_to_buffer_coords(gtk.TEXT_WINDOW_LEFT,
                 event.x, event.y)
            titer, height = self.get_line_at_y(bc[1])
            eiter = titer.copy()
            eiter.forward_to_line_end()
            marks = buf.get_markers_in_region(titer, eiter)
            linenumber = titer.get_line() + 1
            filename = buf.get_filename()
            print linenumber
            if len(marks):
                index = int(marks[0].get_name())
                self.cb.session_manager.delete_breakpoint([index], False)
            else:
                self.cb.session_manager.set_breakpoint(filename, '', linenumber,
                                                   True, '')

    def set_breakpoint(self, index, titer):
        buf = self.get_buffer()
        buf.create_marker(str(index), 'bp', titer)


    def set_buffer(self, buf):
        edit.gtksourceview.SourceView.set_buffer(self, buf)
    
class SourceViewer(PGDSlaveDelegate):

    def create_toplevel_widget(self):
        self._files = {}
        nb = self.add_widget('notebook', gtk.Notebook())
        nb.set_show_tabs(False)
        return nb

    def attach_slaves(self):
        self.main_window.attach_slave('source_holder', self)
        self.show_all()

    def goto(self, filename, linenumber):
        def _v(editor, linenumber):
            self._goto_line(editor, linenumber)
        if filename in self._files:
            def _u(filename, linenumber):
                editor, vbox = self._files[filename]
                self.notebook.set_current_page(self.notebook.page_num(vbox))
                gobject.idle_add(_v, editor, linenumber)
        else:
            def _u(filename, linenumber):
                editor, vbox = self._open_file(filename)
                self._files[filename] = (editor, vbox)
                self.notebook.set_current_page(self.notebook.page_num(vbox))
                gobject.idle_add(_v, editor, linenumber)
        gobject.idle_add(_u, filename, linenumber)

    def _open_file(self, filename):
        vbox, editor = self.create_widget(filename)
                       #self.create_action_group())
        self.notebook.append_page(vbox)
        return editor, vbox

    def create_widget(self, filename):
        vbox = gtk.VBox(spacing=12)
        vbox.show()
        scroller = gtk.ScrolledWindow()
        scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroller.show()
        vbox.add(scroller)
        editor = view = Culebra(self)
        buff = edit.CulebraBuffer(filename)
        if filename is not None:
            buff.load_from_file()
        view.set_buffer(buff)
        editor.set_name("editor")
        editor.show()
        scroller.add(editor)
        return vbox, editor

    def set_breakpoint(self, index, filename, linenumber):
        self.goto(filename, linenumber)
        def _u(index, filename, linenumber):
            editor, vbox = self._files[filename]
            buf = editor.get_buffer()
            titer = buf.get_iter_at_line(linenumber - 1)
            editor.set_breakpoint(index, titer)
        gobject.idle_add(_u, index, filename, linenumber)

    def remove_breakpoint(self, index, filename):
        if filename in self._files:
            editor, vbox = self._files[filename]
            buf = editor.get_buffer()
            buf.delete_marker(buf.get_marker(str(index)))


    def _goto_line(self, editor, linenumber):
        view = editor
        buff = editor.get_buffer()
        # Get line iterator
        line_iter = buff.get_iter_at_line(linenumber - 1)
        # Move scroll to the line iterator
        view.scroll_to_iter(line_iter, 0.25)
        # Place the cursor at the begining of the line
        buff.place_cursor(line_iter)
