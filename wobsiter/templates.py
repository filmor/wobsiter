from Cheetah.Template import Template
from Cheetah.Filters import Filter

from os import path, walk, sep

class EncodeUnicode(Filter):
    def filter(self, val, **kw):
        if type(val) == type(u''):
            return val.encode(kw.get('encoding', 'utf-8'))
        else:
            return str(val)

def get_template(file_path, template_dir=None):
    if not template_dir:
        # TODO
        template_dir = path.join(path.dirname(str(file_path)), "templates")

    res = [template_dir, "index.tmpl"]
    for root, dirs, files in walk(template_dir, topdown=False):
        template_path = root.split(sep)[1:]
        if template_path == file_path[:-1]:
            # TODO
            res = [template_dir] + template_path + ["index.tmpl"]
            break
    return Template(file=path.join(*res), filter=EncodeUnicode)

