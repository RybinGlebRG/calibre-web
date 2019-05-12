from lxml import etree
import uploader
import os
import base64
import sys


class FB2_MetadataExtractor:

    def __init__(self):
        # Needed to distinguish between 2.x and 3.x python versions
        # Code for 2.x is taken from old fb2.py file
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
            return author.decode('utf-8')

    def extract_title(self, tree, ns):
        title = None
        if self.python_major_version >= 3:
            title = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:book-title/text()', namespaces=ns)
            if len(title):
                title = title[0]
            else:
                title = ''
            return title
        else:
            title = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:book-title/text()', namespaces=ns)
            if len(title):
                title = str(title[0].encode('utf-8'))
            else:
                title = u''
            return title.decode('utf-8')

    def extract_description(self, tree, ns):
        description = None
        if self.python_major_version >= 3:
            description = tree.xpath('/fb:FictionBook/fb:description/fb:publish-info/fb:book-name/text()',
                                     namespaces=ns)
            if len(description):
                description = description[0]
            else:
                description = ''
            return description
        else:
            description = tree.xpath('/fb:FictionBook/fb:description/fb:publish-info/fb:book-name/text()',
                                     namespaces=ns)
            if len(description):
                description = str(description[0].encode('utf-8'))
            else:
                description = u''
            return description.decode('utf-8')

    # Extract cover page from XML tree to tmp_file_dir using namespaces ns and return extracted file name
    def extract_coverpage(self, tree, ns, tmp_file_dir):
        if self.python_major_version >= 3:
            # Get coverpage section
            coverpages = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:coverpage', namespaces=ns)
            if len(coverpages) == 0:
                return None
            coverpage = coverpages[0]
            # Get first image section
            images = coverpage.xpath('./fb:image', namespaces=ns)
            if len(images) == 0:
                return None
            image = images[0]
            # Get image file name
            image_file = image.xpath('./@l:href', namespaces=ns)
            image_file = image_file[0]
            # Extract only included binary files
            if image_file[0] != '#':
                return None
            # Get image file name
            image_file_id = image_file[1:]
            # Get base64 encoded image
            binary_files = tree.xpath('/fb:FictionBook/fb:binary[@id="' + image_file_id + '"]', namespaces=ns)
            if len(binary_files) == 0:
                return None
            binary_file = binary_files[0]
            binary_file = binary_file.xpath('./text()', namespaces=ns)
            if len(binary_file) == 0:
                return None
            binary_file = binary_file[0]
            if len(binary_file) == 0:
                return None
            binary_file = str(binary_file)
            # Decode image data
            binary_file = base64.b64decode(binary_file)
            # Write image data to file
            file = open(os.path.join(tmp_file_dir, image_file_id), 'wb')
            file.write(binary_file)
            file.close()
            # Return file name
            return os.path.join(tmp_file_dir, image_file_id)
        else:
            return None

    def get_tree(self, tmp_file_path):
        tree = None
        if self.python_major_version >= 3:
            # Get ElementTree object
            tree = etree.parse(tmp_file_path)
            # Get root Element object
            tree = tree.getroot()
        else:
            fb2_file = open(tmp_file_path)
            tree = etree.fromstring(fb2_file.read())
        return tree

    def extract(self, tmp_file_path, original_file_extension):
        # Get XML tree from XML file
        tree = self.get_tree(tmp_file_path)
        # Extract metadata from XML file using namespaces self.ns
        author = self.extract_author(tree, self.ns)
        title = self.extract_title(tree, self.ns)
        description = self.extract_description(tree, self.ns)
        coverpage = self.extract_coverpage(tree, self.ns, os.path.dirname(tmp_file_path))
        # Fill not extracted values
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
