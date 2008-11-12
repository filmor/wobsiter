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
from ..util import change_ext

class MenuHandler(object):
    def __init__(self, path):
        self._path = path

    def build(self, output):
        from ConfigParser import ConfigParser
        cfg = ConfigParser()
        cfg.read(self._path)

        self.title = cfg.sections()[0]
        self.items =[(n.capitalize(), change_ext(fn, 'html'))
                      for n, fn in cfg.items(self.title)]
        return self

