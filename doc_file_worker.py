import json
import os

_doc_files = {}

__data_path = "resources/doc_text/doc_json.json"


def save_changes():
    with open(__data_path, "w", encoding="utf-8") as write_file:
        json.dump(_doc_files, write_file)


def get_doc_files():
    global _doc_files
    if len(_doc_files) != 0:
        return _doc_files
    if not os.path.exists(__data_path):
        with open(__data_path, "w", encoding="utf-8") as write_file:
            json.dump({'Собственный текст': ''}, write_file)
    with open(__data_path, "r", encoding="utf-8") as read_file:
        _doc_files = dict(json.load(read_file))
    return _doc_files


def add_file(doc_name: str, file_name: str, text: str):
    if doc_name not in _doc_files.keys():
        file_name = file_name.split('.')[0]
        _doc_files[doc_name] = file_name
        save_changes()
        save_file(file_name, text)
        return True
    else:
        return False


def save_file(file_name: str, text: str):
    txt_path = f'resources/doc_text/{file_name}.txt'
    if not os.path.exists(txt_path):
        with open(txt_path, "w", encoding="utf-8") as write_file:
            write_file.write(text)


def get_doc_name():
    return list(_doc_files.keys())
