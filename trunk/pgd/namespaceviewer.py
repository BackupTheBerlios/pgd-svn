
import gtk

import cgi

from components import PGDSlaveDelegate

from tree import Tree


class NamespaceItem(object):

    def __init__(self, nsdict):
        self.name = nsdict['name']
        self.stype = nsdict['type']
        self.srepr = nsdict['repr']
        self.expr = nsdict['expr']
        self.n_subnodes = nsdict['n_subnodes']
        self.key = self.name
        self.is_value = False
    
    def get_markup(self):
        if self.is_value:
            mu = cgi.escape(self.srepr)
        else:
            n = cgi.escape(self.name)
            t = cgi.escape(self.stype)
            mu = ('<tt><b>%s</b>  </tt>'
                  '<span color="#903030"><i>%s</i></span>'
                  % (n, t))
        return mu
    markup = property(get_markup)


class NamespaceTree(Tree):

    SORT_CONTROLS = True
    SORT_AVAILABLE = [('Name', 'name'),
                      ('Type', 'stype')]


class NamespaceViewer(PGDSlaveDelegate):

    def create_toplevel_widget(self):
        toplevel = gtk.VBox()
        t = self.add_widget('tree', NamespaceTree())
        t.set_property('markup-format-string', '%(markup)s')
        toplevel.pack_start(t)
        v = self.add_widget('tree_view', t.view)
        return toplevel

    def update_namespace(self, expr=None, parent=None):
        if expr is None:
            expr = self.get_root_expr()
            parent = None
            self.tree.clear()
        el = [(expr, True)]
        filt = None
        ns = self.session_manager.get_namespace(el, filt)
        for sn in ns[0]['subnodes']:
            item = NamespaceItem(sn)
            valitem = NamespaceItem(sn)
            valitem.is_value = True
            piter = self.tree.add_item(item, parent=parent)
            self.tree.add_item(valitem, parent=piter)

    def on_tree_view__row_expanded(self, tv, titer, path):
        value = self.tree.get(titer, 1).value
        if self.tree.model.iter_n_children(titer) == 1:
            self.update_namespace(value.expr, titer)

    def get_root_expr(self):
        raise NotImplementedError


class GlobalViewer(NamespaceViewer):

    def get_root_expr(self):
        return 'globals()'


class LocalViewer(NamespaceViewer):

    def get_root_expr(self):
        return 'locals()'


class AllNamespaceViewer(PGDSlaveDelegate):

    def create_toplevel_widget(self):
        self.local_viewer = LocalViewer(self.app)
        self.global_viewer = GlobalViewer(self.app)
        tl = gtk.VBox()
        nb = gtk.Notebook()
        tl.pack_start(nb)
        nb.set_tab_pos(gtk.POS_TOP)
        lh = self.add_widget('globals_holder', gtk.EventBox())
        tl1 = self._create_big_label('globals()')
        nb.append_page(lh, tab_label=tl1)
        gh = self.add_widget('locals_holder', gtk.EventBox())
        tl2 = self._create_big_label('locals()')
        nb.append_page(gh, tab_label=tl2)
        return tl

    def _create_big_label(self, text):
        l = gtk.Label()
        mu = ('<b>%s</b>'
              % cgi.escape(text))
        l.set_markup(mu)
        return l

    def attach_slaves(self):
        self.attach_slave('globals_holder', self.global_viewer)
        self.attach_slave('locals_holder', self.local_viewer)
        self.main_window.attach_slave('ns_holder', self)
        self.show_all()

    def update_namespace(self):
        self.local_viewer.update_namespace()
        self.global_viewer.update_namespace()


