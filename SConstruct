
from docutils import core
from docutils import writers
from docutils.utils import SystemMessage

# TODO Configuration
# TODO Make HTMLs dependent of the templates
# TODO Support for subdirectories
# TODO Support for blogging (as a SConscript)
# TODO Manage downloadable files and make their links usable in the ReST
# TODO Syntax highlighting using pygments

template_dir = "templates"
output_dir = ARGUMENTS.get("output", "output")
site_dir = "site"
site_title = "Benedikts Seite"

def html_parts(name, **kwargs):
    f = file(name)
    overrides = {
            'doctitle_xform' : True,
            'initial_header_level' : 1,
            'halt_level' : 2,
            'cloak_email_addresses' : True,
            'stylesheet' : '',
            '_stylesheet_required' : False,
            'embed_stylesheet' : False,
            }
    overrides.update(kwargs)
    try:
        return core.publish_parts(f.read(), source_path=name,
                                  writer_name='html', settings_overrides=overrides)
    except SystemMessage, msg:
        print msg
        import sys
        sys.exit(1)

from Cheetah.Template import Template
from Cheetah.Filters import Filter

import os

class EncodeUnicode(Filter):
    def filter(self, val, **kw):
        if type(val) == type(u''):
            return val.encode(kw.get('encoding', 'utf-8'))
        else:
            return str(val)

def get_template(path):
    res = [template_dir, "index.tmpl"]
    for root, dirs, files in os.walk(template_dir, topdown=False):
        template_path = root.split(os.sep)[1:]
        if template_path == path[:-1]:
            # TODO
            res = [template_dir] + template_path + ["index.tmpl"]
            break
    return Template(file=os.path.join(*res), filter=EncodeUnicode)

def build_rst(target, source, env):
    parts = [html_parts(str(input)) for input in source]

    menu = zip((i['title'] for i in parts),
               (str(i)[len(output_dir)+len(os.sep):] for i in target))

    title = site_title

    for target, parts in zip(target, parts):
        template = get_template(str(target).split(os.sep)[1:])

        template.title = title
        template.menu = menu
        template.subtitle = parts['title']
        template.keywords = ''
        template.description = ''
        template.index_content = parts['body']

        print >> file(str(target), 'w'), template

def emitter(target, source, env):
    source.sort(cmp =
            lambda x,y : cmp(os.path.split(str(x))[1], os.path.split(str(y))[1])
            )
    output_dir = str(target[0])
    new_targets = []
    for i in source:
        dirname, basename = os.path.split(str(i))
        name = basename[:basename.rfind('.')].lstrip("1234567890_") + ".html"
        new_targets.append(File(os.path.join(output_dir, name)))
    return new_targets, source

# cheetah_builder
rst_builder = Builder(action=build_rst, suffix='', src_suffix='.txt', emitter=emitter)

env = Environment(BUILDERS={'ReST':rst_builder})

env.ReST(Dir(output_dir), Glob(os.path.join(site_dir, "*.txt")))

