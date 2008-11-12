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
from .. import util
from os import walk
from file import FileHandler
from . import Source

from Cheetah.Template import Template
from Cheetah.Filters import Filter

class EncodeUnicode(Filter):
    def filter(self, val, **kw):
        if type(val) == type(u''):
            return val.encode(kw.get('encoding', 'utf-8'))
        else:
            return str(val)

class TemplateHandler(object):
    def __init__(self, path):
        self._path = path
        self.deps = []
        for p, _, files in walk(util.dirname(self._path)):
            new_p = p[p.find('/'):]
            new_p = new_p[1:]
            self.deps += [Source(util.join(p, f), handler=FileHandler,
                                 dir=new_p)
                          for f in files
                          if util.ext(f) != 'tmpl']

    def build(self, _):
        return Template(file=self._path, filter=EncodeUnicode)
