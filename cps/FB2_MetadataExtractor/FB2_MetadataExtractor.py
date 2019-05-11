from lxml import etree
import uploader
import os
import base64
import sys


class FB2_MetadataExtractor:

    def __init__(self):
        self.python_major_version = sys.version_info.major
        self.ns = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0',
                   'l': 'http://www.w3.org/1999/xlink',
                   }

    def extract_author(self, tree, ns):
        if self.python_major_version >= 3:
            authors = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:author', namespaces=ns)

            def get_author(element):
                last_name = element.xpath('fb:last-name/text()', namespaces=ns)
                if len(last_name):
                    last_name = last_name[0]
                else:
                    last_name = ''
                middle_name = element.xpath('fb:middle-name/text()', namespaces=ns)
                if len(middle_name):
                    middle_name = middle_name[0]
                else:
                    middle_name = ''
                first_name = element.xpath('fb:first-name/text()', namespaces=ns)
                if len(first_name):
                    first_name = first_name[0]
                else:
                    first_name = ''
                full_name = first_name + ' ' + middle_name + ' ' + last_name

                return full_name

            author = ', '.join(map(get_author, authors))
            return author
        else:
            authors = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:author', namespaces=ns)

            def get_author(element):
                last_name = element.xpath('fb:last-name/text()', namespaces=ns)
                if len(last_name):
                    last_name = last_name[0].encode('utf-8')
                else:
                    last_name = u''
                middle_name = element.xpath('fb:middle-name/text()', namespaces=ns)
                if len(middle_name):
                    middle_name = middle_name[0].encode('utf-8')
                else:
                    middle_name = u''
                first_name = element.xpath('fb:first-name/text()', namespaces=ns)
                if len(first_name):
                    first_name = first_name[0].encode('utf-8')
                else:
                    first_name = u''
                return (first_name.decode('utf-8') + u' '
                        + middle_name.decode('utf-8') + u' '
                        + last_name.decode('utf-8')).encode('utf-8')

            author = str(", ".join(map(get_author, authors)))
            return author

    def extract_title(self, tree, ns):
        # TODO: Add
        return None

    def extract_description(self, tree, ns):
        # TODO: Add
        return None

    def extract_coverpage(self, tree, ns):
        # TODO: Add
        return None

    def get_tree(self, tmp_file_path):
        tree = None
        if self.python_major_version >= 3:
            tree = etree.parse(tmp_file_path)
            tree = tree.getroot()
        else:
            fb2_file = open(tmp_file_path)
            tree = etree.fromstring(fb2_file.read())
        return tree

    def extract(self, tmp_file_path, original_file_extension):
        tree = self.get_tree(tmp_file_path)
        author = self.extract_author(tree, self.ns)
        title = self.extract_title(tree, self.ns)
        description = self.extract_description(tree, self.ns)
        coverpage = self.extract_coverpage(tree, self.ns)
        tags = ""
        series = ""
        series_id = ""
        languages = ""

        return uploader.BookMeta(
            file_path=tmp_file_path,
            extension=original_file_extension,
            title=title,
            author=author,
            cover=coverpage,
            description=description,
            tags=tags,
            series=series,
            series_id=series_id,
            languages=languages)
