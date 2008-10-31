#!/usr/bin/env python
# TODO Configuration
# TODO Make HTMLs dependent of the templates
# TODO Support for subdirectories
# TODO Support for blogging (as a SConscript)
# TODO Manage downloadable files and make their links usable in the ReST
# TODO Syntax highlighting using pygments

from __future__ import with_statement
from wobsiter import Source, Output, Path, glob, TemplateFinder
from sys import argv

#from optparse import ConfigParser

template_dir = Path("templates")
site_dir = Path("site")

with Output("file://output") as output:
    for i in glob(site_dir / '*.txt'):
        Source(i, template=TemplateFinder(template_dir)(i))(output)

