from docutils import core
from docutils.utils import SystemMessage
from glob import glob
from os.path import join
from os import sep

from templates import TemplateFinder

class lazy_property(object):
    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.func_name, value)
        return value
    

class WobsiteBuilder(object):
    def __init__(self, **options):
        self.site_dir = options['site_dir']
        self.template_finder = TemplateFinder(options['template_dir'])
        self.title = options['title']

    @lazy_property
    def parts(self):
        result = {}
        overrides = {
                'doctitle_xform' : True,
                'initial_header_level' : 1,
                'halt_level' : 2,
                'cloak_email_addresses' : True,
                'stylesheet' : '',
                '_stylesheet_required' : False,
                'embed_stylesheet' : False,
            }
    
        for f in glob(join(self.site_dir, '*.txt')):
            print f
            name = f[f.find(sep)+1:f.rfind('.')].lstrip('0123456789')
            result[name] = core.publish_parts(file(f).read(), source_path=f,
                                              writer_name='html',
                                              settings_overrides=overrides)
        return result


    def build_directory(self, output_dir):
        EXT = '.html'

        menu = zip((i['title'] for i in self.parts.itervalues()),
                   (i + EXT for i in self.parts))

        title = self.title

        for name, parts in self.parts.iteritems():
            template = self.template_finder(name)

            template.title = self.title
            template.menu = menu
            template.subtitle = parts['title']
            template.keywords = ''
            template.description = ''
            template.index_content = parts['body']

            print join(output_dir, name + EXT)

            print >> file(join(output_dir, name + EXT), 'w'), template

