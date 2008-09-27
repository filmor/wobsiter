# TODO Configuration
# TODO Make HTMLs dependent of the templates
# TODO Support for subdirectories
# TODO Support for blogging (as a SConscript)
# TODO Manage downloadable files and make their links usable in the ReST
# TODO Syntax highlighting using pygments

import os.path

from wobsiter import build_rst

template_dir = os.path.join("site", "templates")
output_dir = ARGUMENTS.get("output", "output")
site_dir = "site"
site_title = "Benedikts Seite"

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

