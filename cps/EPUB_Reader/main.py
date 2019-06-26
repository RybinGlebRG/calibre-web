import io
import os
import base64
import json
import zipfile
from lxml import etree
from EPUB_Reader import EPUB_Parser, FileManager


class EPUB_Reader:

    def __init__(self, render_routine, db, config):
        self.render_routine = render_routine
        self.db = db
        self.config = config

    def unzip(self, book, dir):
        path = os.path.join(self.config.config_calibre_dir, book.path)
        target = None
        # dir = os.path.join(self.config.config_main_dir, 'temp')

        for file in os.listdir(path):
            if file.endswith("epub"):
                target = os.path.join(path, file)
                break

        if os.path.exists(dir):
            for root, dirs, files in os.walk(dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        else:
            os.mkdir(dir)

        zip_file = zipfile.ZipFile(target, 'r')
        zip_file.extractall(dir)
        zip_file.close()

    def prepare_files(self, file_path):
        epub_parser = EPUB_Parser.EPUB_Parser()
        file_manager = FileManager.FileManager()

        # Find all needed files
        epub_parser.load_tree(file_path)
        additional_files_names = epub_parser.get_additional_files_names()

        # Get all found files
        files = file_manager.collect_files(additional_files_names, os.path.basename(file_path),
                                           os.path.dirname(file_path))

        head_children = epub_parser.extract_head_children(files[os.path.basename(file_path)]["data"])
        body_children = epub_parser.extract_body_children(files[os.path.basename(file_path)]["data"])

        # Serialize
        result = json.dumps(files)
        result = "<html><head>"+head_children+"</head>"+"<body>"+body_children+"</body></html>"
        return result

    def get_content_list(self, dir):
        meta_inf_path = os.path.join(dir, 'META-INF')
        meta_inf_path = os.path.join(meta_inf_path, 'container.xml')
        tree = etree.parse(meta_inf_path)
        # Get root Element object
        tree = tree.getroot()

        ns = {"ns": tree.nsmap[None]}
        # print(etree.tostring(tree, pretty_print=True))

        rootfiles = tree.xpath('//ns:rootfile', namespaces=ns)
        rootfile = rootfiles[0]
        rootfile = rootfile.xpath('./@full-path')[0]
        rootfile = os.path.join(dir, rootfile)

        tree = etree.parse(rootfile)
        tree = tree.getroot()
        ns = {"ns": tree.nsmap[None]}
        files = tree.xpath('//ns:item', namespaces=ns)

        return files

    def get_first_file(self, dir):
        files = self.get_content_list(dir)
        result = None
        href = None
        for file in files:
            href = file.xpath('./@href')[0]
            tmp1, tmp2 = os.path.splitext(href)
            # TODO: Provide support for images
            if tmp2[1:].upper() not in ['JPG', 'JPEG', 'PNG']:
                result = href
                break

        return result

    def get_specific_file(self, file_name, dir):
        files = self.get_content_list(dir)
        result = None
        href = None
        for file in files:
            href = file.xpath('./@href')[0]
            basename = os.path.basename(href)
            if basename == file_name:
                result = href
        return result

    def get_next_file(self, file_name, dir):
        files = self.get_content_list(dir)
        result = None
        href = None
        is_exit = False
        for file in files:
            href = file.xpath('./@href')[0]
            basename = os.path.basename(href)
            if is_exit:
                result = href
                break
            if basename == file_name:
                is_exit = True
        return result

    def get_previous_file(self,file_name,dir):
        files = self.get_content_list(dir)
        result = None
        href = None
        previous = None
        for file in files:
            href = file.xpath('./@href')[0]
            basename = os.path.basename(href)
            if basename == file_name and previous is not None:
                return previous
            elif basename == file_name and previous is None:
                return href
            previous = href

    def epub_book(self, book_id, section_from=None, section_to=None, file_name=None, is_next=False,
                  is_previous=False):
        book = self.db.session.query(self.db.Books).filter(self.db.Books.id == book_id).first()

        dir = os.path.join(self.config.config_main_dir, 'temp')

        self.unzip(book, dir)

        href = None

        if file_name is None:
            href = self.get_first_file(dir)
        elif file_name is not None and not is_next and not is_previous:
            href = self.get_specific_file(file_name, dir)
        elif file_name is not None and is_next and not is_previous:
            href = self.get_next_file(file_name, dir)
        elif file_name is not None and is_previous and not is_next:
            href = self.get_previous_file(file_name,dir)

        file_path = os.path.join(dir, href)

        result = self.prepare_files(file_path)

        return result

    def epub_reader(self, book_id):
        return self.render_routine('/epub_reader/read.html', book_id=book_id, title=u"Read a Book")
