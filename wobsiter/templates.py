
from util import Path
from os import path, walk, sep
from source import Source


class TemplateFinder(object):
    def __init__(self, template_dir):
        self.template_dir = str(template_dir)

    def __call__(self, file_path):
        file_path = str(file_path)
        template_dir = self.template_dir
        res = [template_dir, "index.tmpl"]
        for root, dirs, files in walk(template_dir, topdown=False):
            template_path = root.split(sep)[1:]
            if template_path == file_path[:-1]:
                # TODO
                res = [template_dir] + template_path + ["index.tmpl"]
                break
        return Source(Path(path.join(*res)))

