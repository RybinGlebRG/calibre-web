import io
import os
import base64
import json
# from lxml import etree
from EPUB_Reader import EPUB_Parser, FileManager


class EPUB_Reader:

    def __init__(self):
        pass

    def test(self):
        file_name = 'C:\\Users\\Gleb\\Downloads\\Sato Tsutomu, Ishida Kana_Mahouka Koukou no Rettousei, Vol.1\\index_split_001.xhtml'

        epub_parser = EPUB_Parser.EPUB_Parser()
        file_manager = FileManager.FileManager()

        # Find all needed files
        epub_parser.load_tree(file_name)
        additional_files_names = epub_parser.get_additional_files_names()

        # Get all found files
        files = file_manager.collect_files(additional_files_names, os.path.basename(file_name), os.path.dirname(file_name))

        # Serialize
        result = json.dumps(files)
        return result

    def test2(self):
        file_name = 'D:\\Pycharm_Projects\\calibre-web\\cps\\EPUB_Reader\\templates\\read.html'
        f = io.open(file_name, mode='r', encoding='utf-8')
        text = f.read()
        return
