from lxml import etree
import os
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import re


class EPUB_Parser:

    def __init__(self):
        self.tree = None

    def load_tree(self, file_name):
        parser = etree.HTMLParser()
        self.tree = etree.parse(file_name, parser)

    def determine_type(self, file_name):
        basename = os.path.basename(file_name)
        tmp1, tmp2 = os.path.splitext(basename)
        suffix = tmp2[1:].upper()
        if suffix in ["CSS"]:
            return "STYLE"
        if suffix in ["PNG", "JPG", "JPEG"]:
            return "IMAGE"

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
            res["type"] = self.determine_type(file)
            files.append(res)
        images = tree.xpath('//img')
        for image in images:
            file = image.xpath('./@src')[0]
            res = {}
            res["data"] = file
            res["main"] = False
            res["type"] = self.determine_type(file)
            files.append(res)
        return files

    def extract_head_children(self, string):
        result = re.search(r'<head>', string, re.IGNORECASE)
        start = result.end()
        result = re.search(r'</head>', string, re.IGNORECASE)
        end = result.start()
        head = string[start:end].strip()
        return head

    def extract_body_children(self, string):
        result = re.search(r'<body[^>]*>', string, re.IGNORECASE)
        start = result.end()
        result = re.search(r'</body>', string, re.IGNORECASE)
        end = result.start()
        body = string[start:end].strip()
        return body

    def extract_body_attributes(self,string):
        result = re.search(r'<body[^>]*>', string, re.IGNORECASE)
        start = result.start()+len("<body")
        end = result.end()-len(">")
        body_attributes = string[start:end].strip()
        return body_attributes
