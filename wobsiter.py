#!/usr/bin/env python
# 
# Copyright 2008 Benedikt Sauer
# 
# This file is part of Wobsiter.
#
# Wobsiter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wobsiter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wobsiter. If not, see <http://www.gnu.org/licenses/>.
# 
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

