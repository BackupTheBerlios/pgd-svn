#!/usr/bin/env python


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
