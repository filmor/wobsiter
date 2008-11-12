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
from __future__ import with_statement
from .. import util
from . import Source
from .file import FileHandler
from .menu import MenuHandler

from docutils.core import publish_parts
from docutils.parsers.rst import roles, nodes
from os.path import basename

from urlparse import urljoin
from re import compile

__all__ = ['RstHandler']

MENUFILE = 'wobsite.menu'

_overrides = {
                'doctitle_xform' : True,
                'initial_header_level' : 1,
                'halt_level' : 2,
                'cloak_email_addresses' : True,
                'stylesheet' : '',
                '_stylesheet_required' : False,
                'embed_stylesheet' : False,
            }

_link_regex = compile('(?P<name>.*) <(?P<link>.*)>')

def _parse_ref(string):
    m = _link_regex.match(string)
    return (m.group(1), m.group(2))

def file_role(role, rawtext, text, lineno, inliner, options={}, content={}):
    source = inliner.document.settings._source
    path = text
    name = util.basename(text)
#    name, link = _parse_ref(text)
#    file_dir = inliner.document.settings.file_directory
    file_dir = "files"
    source.deps += (Source(path, dir=file_dir, handler=FileHandler),)
    ref = file_dir + '/' + name #urljoin(file_dir, name)
    node = nodes.reference(rawtext, name, refuri=ref, **options)
    return [node], []

roles.register_canonical_role('file', file_role)
roles.register_canonical_role('script', file_role)


class RstHandler(object):
    EXT = 'txt'
    def __init__(self, path, template, menu=None):
        self._path = path
        self._menu = menu or Source(util.join(util.dirname(path), MENUFILE),
                                    handler=MenuHandler)
        self._template = template
        self.deps = (self._menu, self._template)
        self.filename = util.change_ext(util.basename(path), 'html')
        # BAAAD Hack!! (self really should be in a settings arg of some
        # kind, definately not source_path
        self._parts = publish_parts(file(path).read(), source_path=self,
                                    writer_name='html',
                                    settings_overrides=_overrides)

    def build(self, output):
        template = self._template.result
        parts = self._parts
        menu = self._menu.result
        template.title = menu.title
        template.menu = menu.items
        template.subtitle = parts['title']
        template.keywords = ''
        template.description = ''
        template.index_content = parts['body']

        output.write_file(self.filename, str(template))
