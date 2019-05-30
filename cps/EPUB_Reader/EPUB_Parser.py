from lxml import etree


class EPUB_Parser:

    def __init__(self):
        self.tree = None

    def load_tree(self, file_name):
        parser = etree.HTMLParser()
        self.tree = etree.parse(file_name, parser)

    def get_additional_files_names(self):
        # Get root Element object
        tree = self.tree.getroot()
        files = []
        links = tree.xpath('//link')
        for link in links:
            file = link.xpath('./@href')[0]
            res = {}
            res["data"] = file
            res["main"] = False
            files.append(res)
        return files
