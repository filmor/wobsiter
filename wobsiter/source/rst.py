from __future__ import with_statement
from ..util import lazy_property
from . import Source
from menu import MenuHandler

MENUFILE = 'wobsite.menu'

def make_parts(path, **p_overrides):
    from docutils.core import publish_parts
    overrides = {
                    'doctitle_xform' : True,
                    'initial_header_level' : 1,
                    'halt_level' : 2,
                    'cloak_email_addresses' : True,
                    'stylesheet' : '',
                    '_stylesheet_required' : False,
                    'embed_stylesheet' : False,
                }.update(p_overrides)
    return publish_parts(file(path).read(), source_path=path,
                         writer_name='html', settings_overrides=overrides)

class RstHandler(object):
    EXT = 'txt'
    def __init__(self, path, menu=None, template=None):
        self._path = path
        self._menu = menu or Source(path.dir / MENUFILE, handler=MenuHandler)
        self._template = template or TemplateFinder(path)
        self.deps = (self._menu, self._template)
        self.filename = str(path.base.without_ext) + '.html'

    @lazy_property
    def _parts(self):
        return make_parts(str(self._path))

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

