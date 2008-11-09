from __future__ import with_statement
from ..util import Path
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
    name = basename(text)

#    name, link = _parse_ref(text)

#    file_dir = inliner.document.settings.file_directory
    file_dir = "files"
    source.deps += (Source(Path(path), dir=file_dir, handler=FileHandler),)
    ref = file_dir + '/' + name #urljoin(file_dir, name)
    node = nodes.reference(rawtext, name, refuri=ref, **options)
    return [node], []

roles.register_canonical_role('file', file_role)
roles.register_canonical_role('script', file_role)


class RstHandler(object):
    EXT = 'txt'
    def __init__(self, path, menu=None, template=None):
        self._path = path
        self._menu = menu or Source(path.dir / MENUFILE, handler=MenuHandler)
        self._template = template or TemplateFinder(path)
        self.deps = (self._menu, self._template)
        self.filename = str(path.base.without_ext) + '.html'
        self._parts = publish_parts(file(str(path)).read(), source_path=self,
                                    writer_name='html', settings_overrides=_overrides)

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

