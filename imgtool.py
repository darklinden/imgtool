#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import sys
import datetime
import errno
import random

from PIL import Image

OperationTypeResizeTo = "st"
OperationTypeSizeScale = "ss"
OperationTypeLeftRotate = "lr"
OperationTypeRightRotate = "rr"
OperationTypeFlipX = "fx"
OperationTypeFlipY = "fy"
OperationTypeRepeatTile = "rt"
OperationTypeCenterWithSize = "cs"
OperationTypeAlphaColor = "ac"
OperationTypeAlphaColorAbove = "acb"
OperationTypeGray = "gr"
OperationTypeSplitCutTo = "sct"


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
    return str(datetime.datetime.now().microsecond)

def mkdir_p(path):
    # print("mkdir_p: " + path)
    try:
        os.makedirs(path)
    except OSError as exc:  # Python > 2.5
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

    if OperationTypeResizeTo == o:

        n = str(c).split(",")

        if len(n) != 2:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = int(n[0])
        y = int(n[1])
        img = img.resize((x, y), Image.BILINEAR)
        img.save(path)

    elif OperationTypeSizeScale == o:
        n = str(c).split(",")

        if len(n) != 2:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        x *= float(n[0])
        y *= float(n[1])

        img = img.resize((int(x), int(y)), Image.BILINEAR)
        img.save(path)

    elif OperationTypeLeftRotate == o:
        img = img.transpose(Image.ROTATE_270)
        img.save(path)

    elif OperationTypeRightRotate == o:
        img = img.transpose(Image.ROTATE_90)
        img.save(path)

    elif OperationTypeFlipX == o:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save(path)

    elif OperationTypeFlipY == o:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save(path)

    elif OperationTypeRepeatTile == o:

        n = str(c).split(",")

        if len(n) != 2:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        x = img.size[0]
        y = img.size[1]
        xn = x * int(n[0])
        yn = y * int(n[1])
        newImg = Image.new('RGBA', (xn, yn), (0, 0, 0, 0))
        for xs in range(0, xn, x):
            for ys in range(0, yn, y):
                newImg.paste(img, (xs, ys))

        img = newImg
        img.save(path)

    elif OperationTypeCenterWithSize == o:
        n = str(c).split(",")

        if len(n) == 2:
            xn = int(n[0])
            yn = int(n[1])
            xo = 0
            yo = 0
        elif len(n) == 4:
            xn = int(n[0])
            yn = int(n[1])
            xo = int(n[2])
            yo = int(n[3])

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

        if int(xn) == 0 or int(yn) == 0:
            xn = trueW
            yn = trueH

        newImg = Image.new('RGBA', (xn, yn), (0, 0, 0, 0))

        newImg.paste(img, ((xn / 2) - (trueW / 2) - xLeft + xo, (yn / 2) - (trueH / 2) - yBottom + yo))

        img = newImg
        img.save(path)

    elif OperationTypeAlphaColor == o:

        n = str(c).split(",")

        if len(n) != 3 and len(n) != 4:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        r = int(n[0])
        g = int(n[1])
        b = int(n[2])
        if len(n) == 4:
            a = int(n[3])
        else:
            a = -1

        x = img.size[0]
        y = img.size[1]

        newImg = Image.new('RGBA', (x, y), (0, 0, 0, 0))

        rgb_img = img.convert('RGBA')

        for x0 in range(0, x):
            for y0 in range(0, y):
                isTranparent = False
                pix = rgb_img.getpixel((x0, y0))
                if r == pix[0] and g == pix[1] and b == pix[2]:
                    if a == -1:
                        isTranparent = True
                    elif a == pix[3]:
                        isTranparent = True
                if isTranparent:
                    continue

                newImg.putpixel((x0, y0), pix)

        img = newImg
        img.save(path)

    elif OperationTypeAlphaColorAbove == o:

        n = str(c).split(",")

        if len(n) != 3 and len(n) != 4:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        r = int(n[0])
        g = int(n[1])
        b = int(n[2])
        if len(n) == 4:
            a = int(n[3])
        else:
            a = -1

        x = img.size[0]
        y = img.size[1]

        newImg = Image.new('RGBA', (x, y), (0, 0, 0, 0))

        rgb_img = img.convert('RGBA')

        for x0 in range(0, x):
            for y0 in range(0, y):
                isTranparent = False
                pix = rgb_img.getpixel((x0, y0))
                if pix[0] >= r and pix[1] >= g and pix[2] >= b:
                    if a == -1:
                        isTranparent = True
                    elif pix[3] <= a:
                        isTranparent = True
                if isTranparent:
                    continue

                newImg.putpixel((x0, y0), pix)

        img = newImg
        img.save(path)

    elif OperationTypeGray == o:

        x = img.size[0]
        y = img.size[1]

        newImg = Image.new('RGBA', (x, y), (0, 0, 0, 0))

        rgb_img = img.convert('RGBA')

        for x0 in range(0, x):
            for y0 in range(0, y):
                pix = rgb_img.getpixel((x0, y0))

                red = pix[0]
                green = pix[1]
                blue = pix[2]
                alpha = pix[3]

                avg = (red + green + blue) / 3
                newImg.putpixel((x0, y0), (int(avg), int(avg), int(avg), alpha))

        img = newImg
        img.save(path)

    elif OperationTypeSplitCutTo == o:

        n = str(c).split(",")

        if len(n) != 4:
            print ("constants [" + c + "] is not valid, skipped.")
            return

        sx = int(n[0])
        sy = int(n[1])

        x = img.size[0]
        y = img.size[1]

        ix = 0
        iy = 0
        while sy * iy < y:
            while sx * ix < x:
                one = img.crop((sx * ix, sy * iy, sx * (ix + 1), sy * (iy + 1)))

                file_name, extension = os.path.splitext(path)
                one_path = file_name + time_str() + extension
                one.save(one_path)
                ix += 1
            ix = 0
            iy += 1

        os.remove(path)


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
        print("Operation ResizeTo = \"st\" c = width,height ")
        print("Operation SizeScale = \"ss\" c = xScale,yScale")
        print("Operation LeftRotate = \"lr\"")
        print("Operation RightRotate = \"rr\"")
        print("Operation FlipX = \"fx\"")
        print("Operation FlipY = \"fy\"")
        print("Operation RepeatTileXY = \"rt\" c = xCount,yCount")
        print("Operation CenterWithSize = \"cs\" c = width,height / width,height,xOffset,yOffset")
        print("Operation AlphaSelectColor = \"ac\" c = r,g,b / r,g,b,a")
        print("Operation AlphaSelectColorAbove = \"acb\" c = r,g,b / r,g,b,a")
        print("Operation MakeGrayImage = \"gr\"")
        print("Operation SplitCutTo = \"sct\" c = width,height")

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
                    if fn.lower().endswith(".png") or fn.lower().endswith(".jpg") or fn.lower().endswith(
                            ".gif") or fn.lower().endswith(".bmp") or fn.lower().endswith(".jpeg"):
                        deal_with_image(file_path, _operation, _constant)


if __name__ == "__main__":
    main()
