import os
import urllib
import zipfile


def unescape(value):
    value = value.replace('%u', '\\u')  # 将%uxxxx 替换换 \uxxxx 这才可以进行utf-8解码
    enc_bytes = urllib.parse.unquote_to_bytes(value)  # 返回的 byte
    enc_bytes = enc_bytes.decode('UTF-8')  # decode UTF-8 解码只能解开 \uXXXX 的Unicode 标准形式
    return enc_bytes


def is_all_chinese(strs):
    """判断字符串是否为全中文"""
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def make_zip(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, "w") as zip_file:
        pre_len = len(os.path.dirname(source_dir))
        for parent, dir_names, filenames in os.walk(source_dir):
            for filename in filenames:
                path_file = os.path.join(parent, filename)
                arc_name = path_file[pre_len:].strip(os.path.sep)  # 相对路径
                zip_file.write(path_file, arc_name)
