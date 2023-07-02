a = 5

# print(4 / 5)
# a = input("你奋斗了吗?\n")
a /= 5
# print("%.2f" % a)
# print(float("3.4"))
# print(str(10))
# print(repr(10))

# a = eval("5>3")
# print(a)
# print(ord("a"))
# print(bin(10))
# print()
# if eval("0"):
#     print("love" * 4)
#
# print(type(a))

from zipfile import ZipFile
import os
from pprint import pprint
from pathlib import Path


def extract_zip(src: str, dst: str=None, include=True):
    """
    src     : zip文件的路径
    dst     : 要压缩到哪个文件夹，默认压缩到zip文件所在的文件夹下
    include : 是否将zip文件名作为压缩文件的根目录
    """
    with ZipFile(src) as zip_file:
        name_to_info = zip_file.NameToInfo
        # copy map first
        sign = None
        for name, info in name_to_info.copy().items():
            real_name = name.encode('cp437').decode('gbk')
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info




        print(len(name_to_info))
        # print('/' in list(name_to_info.keys())[0])
        pprint(name_to_info)

        if dst is None:
            dst = Path(src).parent
        else:
            dst = Path(dst)

        # 处理zip根目录是单个文件或者空文件夹
        file_nums = len(name_to_info)
        if file_nums == 1:
            zip_file.extractall(str(dst))
        # 处理zip根目录是单个文件夹
        elif file_nums > 1:
            pass
        if include:
            dst = dst / Path(src).stem
            zip_file.extractall(str(dst))
        else:
            zip_file.extractall(dst)


file_path = r"C:\Users\17634\Desktop\集成算法5.zip"
# file_path = r"C:\Users\17634\Desktop\a.zip"
extract_zip(file_path, r"C:\Users\17634\Desktop\a")