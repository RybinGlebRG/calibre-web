import io
import base64
import os


class FileManager:

    def __init__(self):
        pass

    def load_binary(self, path):
        f = io.open(path, mode='rb')
        text = f.read()
        return text

    def encode(self, text):
        result = base64.encodebytes(text)
        return result

    def get_encoded(self, path):
        binary = self.load_binary(path)
        result = self.encode(binary)
        return result

    def load(self, path):
        f = io.open(path, mode='r', encoding='utf-8')
        text = f.read()
        return text

    def get_file(self, path):
        string = self.load(path)
        return string

    def load_style(self, path):
        loaded_file = self.get_file(path)
        return loaded_file

    def load_image(self, path):
        base64_bytes = self.get_encoded(path)
        base64_string = base64_bytes.decode()
        return base64_string

    def collect_files(self, additional_file_names, main_file_name, directory_name):
        files = {}
        for file in additional_file_names:
            path = os.path.join(directory_name, file["data"])
            loaded_file = None
            if file["type"] == "STYLE":
                loaded_file = self.load_style(path)
            elif file["type"] == "IMAGE":
                loaded_file = self.load_image(path)
            # loaded_file = self.get_file(path)
            content = {}
            content["data"] = loaded_file
            content["main"] = file["main"]
            content["type"] = file["type"]
            files[file["data"]] = content

        path = os.path.join(directory_name, main_file_name)
        loaded_file = self.get_file(path)
        content = {}
        content["data"] = loaded_file
        content["main"] = True
        files[main_file_name] = content
        return files
