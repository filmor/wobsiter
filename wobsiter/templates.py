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

from os import path, walk, sep
from source import Source


class TemplateFinder(object):
    def __init__(self, template_dir):
        self.template_dir = str(template_dir)

    def __call__(self, file_path):
        template_dir = self.template_dir
        res = [template_dir, "index.tmpl"]
        for root, dirs, files in walk(template_dir, topdown=False):
            template_path = root.split(sep)[1:]
            if template_path == file_path[:-1]:
                # TODO
                res = [template_dir] + template_path + ["index.tmpl"]
                break
        return Source(path.join(*res))

