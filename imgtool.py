#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import sys
import datetime
import errno

from PIL import Image

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
OperationTypeCenterWithSize = "cs"

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
    try:
        img = Image.open(path)
    except:
        print ("file [" + path + "] is not valid image, skipped.")
        return

    if OperationTypeSizeAdd == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        x += int(c)
        y += int(c)
        img = img.resize((x, y), Image.BILINEAR)

    elif OperationTypeWidthAdd == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        x += int(c)
        # y += int(c)
        img = img.resize((x, y), Image.BILINEAR)
    elif OperationTypeHeightAdd == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        # x += int(c)
        y += int(c)
        img = img.resize((x, y), Image.BILINEAR)
    elif OperationTypeSizeScale == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        x *= float(c)
        y *= float(c)
        img = img.resize((int(x), int(y)), Image.BILINEAR)
    elif OperationTypeWidthScale == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        x *= float(c)
        # y *= float(c)
        img = img.resize((int(x), int(y)), Image.BILINEAR)
    elif OperationTypeHeightScale == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

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
    elif OperationTypeRepeatTile == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        xn = x * int(c)
        yn = y * int(c)
        newImg = Image.new('RGBA', (xn, yn), (0, 0, 0, 0))
        for xs in range(0, xn, x):
            for ys in range(0, yn, y):
                newImg.paste(img, (xs, ys))

        img = newImg
    elif OperationTypeRepeatTileX == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        xn = x * int(c)
        yn = y # y * int(c)
        newImg = Image.new('RGBA', (xn, yn), (0, 0, 0, 0))
        for xs in range(0, xn, x):
            for ys in range(0, yn, y):
                newImg.paste(img, (xs, ys))

        img = newImg
    elif OperationTypeRepeatTileY == o:
        if int(c) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        xn = x # x * int(c)
        yn = y * int(c)
        newImg = Image.new('RGBA', (xn, yn), (0, 0, 0, 0))
        for xs in range(0, xn, x):
            for ys in range(0, yn, y):
                newImg.paste(img, (xs, ys))
    elif OperationTypeCenterWithSize == o:
        xn, yn = str(c).split(",")
        xn = int(xn)
        yn = int(yn)

        if int(xn) == 0 or int(yn) == 0:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        newImg = Image.new('RGBA', (xn, yn), (0, 0, 0, 0))

        x = img.size[0]
        y = img.size[1]
        rgb_img = img.convert('RGBA')

        xSetFlag = True
        xLeft = 0
        xRight = x
        for x0 in range(0, x):
            yIsTranparent = True
            for y0 in range(0, y):
                pix = rgb_img.getpixel((x0, y0))
                if pix[3] != 0:
                    yIsTranparent = False
                    break
            if x0 > xLeft and yIsTranparent and xSetFlag:
                xLeft = x0
            if not xSetFlag and yIsTranparent and x0 < xRight:
                xRight = x0
                break
            if not yIsTranparent:
                xSetFlag = False

        ySetFlag = True
        yTop = y
        yBottom = 0
        for y0 in range(0, y):
            xIsTranparent = True
            for x0 in range(0, x):
                pix = rgb_img.getpixel((x0, y0))
                if pix[3] != 0:
                    xIsTranparent = False
                    break
            if y0 > yBottom and xIsTranparent and ySetFlag:
                yBottom = y0
            if not ySetFlag and xIsTranparent and y0 < yTop:
                yTop = y0
                break
            if not xIsTranparent:
                ySetFlag = False

        trueW = xRight - xLeft
        trueH = yTop - yBottom

        newImg.paste(img, ((xn / 2) - (trueW / 2) - xLeft, (yn / 2) - (trueH / 2) - yBottom))

        img = newImg

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
        print("Operation RepeatTileXY = \"rt\"")
        print("Operation RepeatTileX = \"rtx\"")
        print("Operation RepeatTileY = \"rty\"")
        print("Operation CenterWithSize = \"cs\"")

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
                    if fn.lower().endswith(".png") or fn.lower().endswith(".jpg") or fn.lower().endswith(".gif") or fn.lower().endswith(".bmp") or fn.lower().endswith(".jpeg"):
                        deal_with_image(file_path, _operation, _constant)


if __name__ == "__main__":
    main()