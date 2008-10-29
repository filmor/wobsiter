
EXT = 'txt'

MENUFILE = 'wobsite.menu'

def make_parts(path, **p_overrides):
    overrides = {
                    'doctitle_xform' : True,
                    'initial_header_level' : 1,
                    'halt_level' : 2,
                    'cloak_email_addresses' : True,
                    'stylesheet' : '',
                    '_stylesheet_required' : False,
                    'embed_stylesheet' : False,
                }.update(p_overrides)

    print 'Processing ', path
    return core.publish_parts(file(path).read(), source_path=path,
                              writer_name='html', settings_overrides=overrides)

class Handler(object):
    def __init__(self, path):
        self._path = path
        self._menu = Source(path.dir / MENUFILE)
        self._template = TemplateFinder(path)
        self.deps = (self._menu, self._template)
        self.filename = str(path.base.without_ext) + '.html'

    @util.lazy_property
    def _parts(self):
        return make_parts(self._path)

    def build(self, output):
        template = self._template.make_template()
        menu = self._menu
        parts = self._parts

        template.title = menu.title
        template.subtitle = parts['title']
        template.keywords = ''
        template.description = ''
        template.index_content = parts['body']

        output.write(self.filename, str(template))

