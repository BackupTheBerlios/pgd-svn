
import gtk

from components import PGDSlaveDelegate

from tree import Tree

class Breakpoint(object):
    
    def __init__(self, index, filename, linenumber):
        self.key = index
        self.filename = filename
        self.linenumber = linenumber
        self.enabled = True

    def get_color(self):
        if self.enabled:
            return '#000000'
        else:
            return '#a0a0a0'

    def get_disabled_text(self):
        if self.enabled:
            return ''
        else:
            return '(disabled)'

    disabled_text = property(get_disabled_text)
    
    color = property(get_color)

class BreakpointViewer(PGDSlaveDelegate):

    def create_toplevel_widget(self):
        vb = gtk.VBox()
        t = self.add_widget('tree', Tree())
        t.set_property('markup-format-string',
                       '<b>[%(key)s]</b>'
                       '<span color="%(color)s">'
                       '<tt> %(filename)s:%(linenumber)s </tt>'
                       '</span><i>%(disabled_text)s</i>')
        vb.pack_start(t)
        return vb

    def attach_slaves(self):
        self.main_window.attach_slave('breaks_holder', self)
        self.show_all()

    def _get_all_index(self, indices):
        mod = self.tree.model
        for index in indices:
            for row in mod:
                if row[0] == str(index):
                    yield index, row
        
    def _get_all_bps(self, indices):
        for index, row in self._get_all_index(indices):
            value = row[1].value
            yield index, value

    def update_bp(self, action, index, indices, filename, linenumber):
        mod = self.tree.model
        if action == 'set':
            gen = self._get_all_bps([index])
            try:
                index, val = gen.next()
                val.filename = filename
                val.linenumber = linenumber
                val.reset_markup()
            except StopIteration:
                bp = Breakpoint(index, filename, linenumber)
                self.tree.add_item(bp)
                self.app.source.set_breakpoint(index, filename, linenumber)
        elif action == 'remove':
            for i, row in self._get_all_index(indices):
                val = row[1].value
                filename = val.filename
                self.app.source.remove_breakpoint(i, filename)
                mod.remove(row.iter)

        elif action == 'disable':
            for i, value in self._get_all_bps(indices):
                value.enabled = False
                value.reset_markup()
        elif action == 'enable':
            for i, value in self._get_all_bps(indices):
                value.enabled = True
                value.reset_markup()

    def on_tree__double_clicked(self, tv, item):
        val = item.value
        if val.enabled:
            func = self.session_manager.disable_breakpoint
        else:
            func = self.session_manager.enable_breakpoint
        gobject.idle_add(func, [val.key], False)
            

            
        

    def toggle_breakpoint(self):
        lineno = self.m_viewer.GetCurrentLine() + 1 
        self.__toggle_breakpoint(lineno)        
        
    def __toggle_breakpoint(self, lineno):
        bpl = self.m_session_manager.get_breakpoints()
        id = self.m_breakpoint_lines.get(lineno, None)
        if id != None:
            bp = bpl.get(id, None)
            
        if (id == None) or (bp == None):
            self.job_post(self.job_set_breakpoint, (self.m_cur_filename, lineno))
            return

    def job_set_breakpoint(self, filename, lineno):
        try:
            self.m_session_manager.set_breakpoint(filename, '', lineno, True, '')
        except (socket.error, rpdb2.CConnectionException):
            pass
        except rpdb2.BadArgument:
            pass
        
    def job_delete_breakpoint(self, id):
        try:
            self.m_session_manager.delete_breakpoint([id], False)
        except (socket.error, rpdb2.CConnectionException):
            pass
        except rpdb2.BadArgument:
            pass

