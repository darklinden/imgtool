#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

import os
import subprocess
import shutil
import sys
import datetime
import errno




OperationTypeSizeAdd = "sa"
OperationTypeWidthAdd = "wa"
OperationTypeHeightAdd = "ha"
OperationTypeSizeScale = "ss"
OperationTypeWidthScale = "ws"
OperationTypeHeightScale = "hs"
OperationTypeLeftRotate = "lr"
OperationTypeRightRotate = "rr"
OperationTypeFlipX  = "fx"
OperationTypeFlipY = "fy"
OperationTypeRepeatTile = "rt"
OperationTypeRepeatTileX = "rtx"
OperationTypeRepeatTileY = "rty"

def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    return out

def self_install(file, des):
    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    if os.path.isfile(to_path):
        os.remove(to_path)

    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

def time_str():
    return str(datetime.datetime.now())

def mkdir_p(path):
    # print("mkdir_p: " + path)
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def deal_with_image(path, o, c):
    img = Image.open(path)

    if OperationTypeSizeAdd == o:
        x = img.size[0]
        y = img.size[1]
        x += int(c)
        y += int(c)
        img = img.resize((x, y), Image.BILINEAR)

    elif OperationTypeWidthAdd == o:
        x = img.size[0]
        y = img.size[1]
        x += int(c)
        # y += int(c)
        img = img.resize((x, y), Image.BILINEAR)
    elif OperationTypeHeightAdd == o:
        x = img.size[0]
        y = img.size[1]
        # x += int(c)
        y += int(c)
        img = img.resize((x, y), Image.BILINEAR)
    elif OperationTypeSizeScale == o:
        x = img.size[0]
        y = img.size[1]
        x *= float(c)
        y *= float(c)
        img = img.resize((int(x), int(y)), Image.BILINEAR)
    elif OperationTypeWidthScale == o:
        x = img.size[0]
        y = img.size[1]
        x *= float(c)
        # y *= float(c)
        img = img.resize((int(x), int(y)), Image.BILINEAR)
    elif OperationTypeHeightScale == o:
        x = img.size[0]
        y = img.size[1]
        # x *= float(c)
        y *= float(c)
        img = img.resize((int(x), int(y)), Image.BILINEAR)
    elif OperationTypeLeftRotate == o:
        img = img.transpose(Image.ROTATE_270)
    elif OperationTypeRightRotate == o:
        img = img.transpose(Image.ROTATE_90)
    elif OperationTypeFlipX  == o:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif OperationTypeFlipY == o:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    # elif OperationTypeRepeatTile == o:
    # elif OperationTypeRepeatTileX == o:
    # elif OperationTypeRepeatTileY == o:

    img.save(path)

def main():

    # self_install
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("imgtool.py", "/usr/local/bin")
        return

    _operation = ""
    _constant = 0
    _path = ""

    idx = 1
    while idx < len(sys.argv):
        cmd_s = sys.argv[idx]
        if cmd_s[0] == "-":
            cmd = cmd_s[1:]
            v = sys.argv[idx + 1]
            if cmd == "f":
                _path = v
            elif cmd == "o":
                _operation = v
            elif cmd == "c":
                _constant = v
            idx += 2
        else:
            idx += 1

    if _path == "" or _operation == "":
        print("using imgtool -f [file/folder path] -o [operation type] -c [constants value] to deal with image")
        print("Operation SizeAdd = \"sa\"")
        print("Operation WidthAdd = \"wa\"")
        print("Operation HeightAdd = \"ha\"")
        print("Operation SizeScale = \"ss\"")
        print("Operation WidthScale = \"ws\"")
        print("Operation HeightScale = \"hs\"")
        print("Operation LeftRotate = \"lr\"")
        print("Operation RightRotate = \"rr\"")
        print("Operation FlipX = \"fx\"")
        print("Operation FlipY = \"fy\"")
        # print("Operation RepeatTile = \"rt\"")
        # print("Operation RepeatTileX = \"rtx\"")
        # print("Operation RepeatTileY = \"rty\"")
        return

    if not str(_path).startswith("/"):
        _path = os.path.join(os.getcwd(), _path)

    if os.path.isfile(_path):
        # back up
        backup_folder = _path + "_backup_" + time_str()
        mkdir_p(backup_folder)
        shutil.copy(_path, os.path.join(backup_folder, os.path.basename(_path)))

        # work
        deal_with_image(_path, _operation, _constant)
    elif os.path.isdir(_path):
        # back up
        backup_folder = _path + "_backup_" + time_str()
        mkdir_p(backup_folder)
        shutil.copytree(_path, os.path.join(backup_folder, os.path.basename(_path)))

        # work
        for root, dirs, files in os.walk(_path):
            sub_files = os.listdir(root)
            for fn in sub_files:
                file_path = root + "/" + fn
                if os.path.isfile(file_path):
                    deal_with_image(file_path, _operation, _constant)


# if __name__ == "__main__":
main()