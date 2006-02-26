
import os

import gtk


def set_stock_icons(st_req, st_path):
    import pkg_resources as pr
    pidareq = pr.Requirement.parse(st_req)
    icon_names = pr.resource_listdir(pidareq, st_path)
    stock_ids = set(gtk.stock_list_ids())
    iconfactory = gtk.IconFactory()
    theme = gtk.icon_theme_get_default()
    listed = theme.list_icons()
    for icon in icon_names:
        iconname = icon.split('.', 1)[0]
        if iconname not in listed:
            iconres = '/'.join(['icons', icon])
            iconpath = pr.resource_filename(pidareq, iconres)
            pixbuf = gtk.gdk.pixbuf_new_from_file(iconpath)
            iconset = gtk.IconSet(pixbuf)
            iconfactory.add(iconname, iconset)
            gtk.icon_theme_add_builtin_icon(iconname, 128, pixbuf)
    iconfactory.add_default()
    return theme, iconfactory

class Icons(object):

    def __init__(self):
        self.theme, self.iconfactory = set_stock_icons('pgd', 'icons')

    def get(self, name, size=16):
        return self.theme.load_icon(name, size, 0)

icons = Icons()


