#!/usr/bin/env python
# TODO Configuration
# TODO Make HTMLs dependent of the templates
# TODO Support for subdirectories
# TODO Support for blogging (as a SConscript)
# TODO Manage downloadable files and make their links usable in the ReST
# TODO Syntax highlighting using pygments

from wobsiter import WobsiteBuilder
from sys import argv

#from optparse import ConfigParser

options = {
        "template_dir": "templates",
        "site_dir": "site",
        "title": "Benedikts Seite",
        }

bld = WobsiteBuilder(**options)

bld.build_directory(argv[1])

