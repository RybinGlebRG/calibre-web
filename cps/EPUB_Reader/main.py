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
        file_name = 'D:\\test\\index_split_001.xhtml'

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
