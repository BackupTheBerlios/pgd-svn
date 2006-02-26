

import gtk

from components import PGDSlaveDelegate

from tree import IconTree
from icons import icons

class StackItem(object):

    def __init__(self, index, filename, linenumber, function, line):
        self.key = index
        self.filename = filename
        self.linenumber = linenumber
        self.funcion = function
        self.line = line
        self.active=False

    def get_color(self):
        if self.active:
            return '#000000'
        else:
            return '#000000'
    color = property(get_color)

    def get_icon(self):
        if self.active:
            return icons.get(gtk.STOCK_NO, 22)
        else:
            return None

    pixbuf = property(get_icon)


class StackViewer(PGDSlaveDelegate):

    def create_toplevel_widget(self):
        toplevel = gtk.VBox()
        t = self.add_widget('tree', IconTree())
        t.set_property('markup-format-string',
                       '<span color="%(color)s">'
                       '<tt><b>%(filename)s %(linenumber)s</b>\n'
                       '%(line)s</tt></span>')
        toplevel.pack_start(t)
        return toplevel

    def attach_slaves(self):
        self.main_window.attach_slave('stack_holder', self)
        self.show_all()

    def update_stack(self, stack):
        self._current_tid = stack['current tid']
        self.tree.clear()
        for i, row in enumerate(stack['stack'][::-1][:-2]):
            fn, ln, fc, tl = row
            stack_item = StackItem(i, fn, ln, fc, tl)
            if i == 0:
                stack_item.active = True
            self.tree.add_item(stack_item)
    
    def select_frame(self, index):
        for i, row in enumerate(self.tree.model):
            val = row[1].value
            val.active = (i == index)
            val.reset_markup()

    def on_tree__double_clicked(self, tv, item):
        index = item.key
        self.session_manager.set_frame_index(index)


