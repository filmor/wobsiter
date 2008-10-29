from docutils import core
from docutils.utils import SystemMessage
from glob import glob
from os.path import join, isfile

from templates import TemplateFinder
from source import SourceDir


class WobsiteBuilder(object):
    def __init__(self, **options):
        self.sources = SourceDir(options['site_dir'])
        self.template_finder = TemplateFinder(options['template_dir'])
        self.title = options['title']

    def build_directory(self, output_dir):
        EXT = '.html'

        p = lambda n: join(output_dir, n)

        menu = list((str(i.parts['title']), i.name + EXT) for i in self.sources)

        title = self.title

        # Hmm, ein Abhaengigkeitsbaum waer toll. Die verschiedenen Quellen dann ueber
        # unterschiedliche Klassen bauen. Dann
        # for source in walk(source_tree, lambda s: not s.has_changed()):
        #     source.write_to(output_dir)
        # Ist aber noch nicht klar, wie man damit das Menue baut.
        #
        for source in self.sources:
            template = self.template_finder(source.name)
            parts = source.parts

            template.title = self.title
            template.menu = menu
            template.subtitle = parts['title']
            template.keywords = ''
            template.description = ''
            template.index_content = parts['body']

            out_path = p(source.name + EXT)

            output = str(template)
            file(out_path, 'w').write(output)

