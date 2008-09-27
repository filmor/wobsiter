from docutils import core
from docutils import writers
from docutils.utils import SystemMessage
import os

from templates import get_template

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


def build_rst(target, source, env):
    parts = [html_parts(str(input)) for input in source]

    #TODO
    output_dir = os.path.dirname(str(target[0]))

    menu = zip((i['title'] for i in parts),
               (str(i)[len(output_dir)+len(os.sep):] for i in target))

    title = ''# site_title

    for target, parts in zip(target, parts):
        template = get_template(str(target).split(os.sep)[1:])

        template.title = title
        template.menu = menu
        template.subtitle = parts['title']
        template.keywords = ''
        template.description = ''
        template.index_content = parts['body']

        print >> file(str(target), 'w'), template

