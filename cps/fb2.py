#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  This file is part of the Calibre-Web (https://github.com/janeczku/calibre-web)
#    Copyright (C) 2018 lemmsh, cervinko, OzzieIsaacs
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

from lxml import etree
import uploader
import os
import base64


def extract_coverpage(tree, ns, tmp_file_dir):
    coverpages = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:coverpage', namespaces=ns)
    if len(coverpages) == 0:
        return None
    else:
        coverpage = coverpages[0]
        images = coverpage.xpath('./fb:image', namespaces=ns)
        if len(images) == 0:
            return None
        image = images[0]
        image_file = image.xpath('./@l:href', namespaces=ns)
        image_file = image_file[0]
        # Extract only included binary files
        if image_file[0] != '#':
            return None
        image_file_id = image_file[1:]
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
        binary_file = base64.b64decode(binary_file)
        file = open(os.path.join(tmp_file_dir, image_file_id), 'wb')
        file.write(binary_file)
        file.close()
        return os.path.join(tmp_file_dir, image_file_id)


def get_fb2_info(tmp_file_path, original_file_extension):
    ns = {
        'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0',
        'l': 'http://www.w3.org/1999/xlink',
    }

    tree = etree.parse(tmp_file_path)
    tree = tree.getroot()

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

    title = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:book-title/text()', namespaces=ns)
    if len(title):
        title = title[0]
    else:
        title = ''
    description = tree.xpath('/fb:FictionBook/fb:description/fb:publish-info/fb:book-name/text()', namespaces=ns)
    if len(description):
        description = description[0]
    else:
        description = ''

    coverpage = extract_coverpage(tree, ns, os.path.dirname(tmp_file_path))

    return uploader.BookMeta(
        file_path=tmp_file_path,
        extension=original_file_extension,
        title=title,
        author=author,
        cover=coverpage,
        description=description,
        tags="",
        series="",
        series_id="",
        languages="")
