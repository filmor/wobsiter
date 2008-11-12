#!/usr/bin/env python
# TODO Configuration
# TODO Syntax highlighting using pygments

from __future__ import with_statement
from wobsiter import Source, Output, TemplateFinder
from sys import argv
from glob import glob
from os.path import join

#from optparse import ConfigParser

template_dir = "templates"
site_dir = "site"

with Output("file://output") as output:
    for i in glob(join(site_dir, '*.txt')):
        Source(i, template=TemplateFinder(template_dir)(i))(output)

