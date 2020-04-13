# -*-coding: utf-8 -*-
import os, sys
import csv
import configparser as cp

path = os.getcwd()
print("dir: " + path)

# フォルダ内探索
def search(csv):
    exi = os.path.exists(csv)
    return exi

# 拡張子チェック
def checker(csv):
    root, ext = os.path.splitext(csv)
    return ext

# 設定ファイル作成
def makeIni(path):
    config = cp.ConfigParser()
    csv = path

    section1 = 'System'
    config.add_section(section1)
    config.set(section1, "path", os.getcwd())
    config.set(section1, "file", os.path.join(os.getcwd(), csv))

    with open('System.ini', 'w') as configfile:
        config.write(configfile)

# 第一処理
def csvOpen():
    print("終了するにはexit")
    print("↓input csvfile name")

    csvFile = input()

    if csvFile == "exit":
        sys.exit(0)

    csvfileDir = os.path.join(path, csvFile)
    print(csvfileDir)

    chk = checker(csvfileDir)
    if chk == ".csv":
        snd = search(csvfileDir)
    else:
        print("This file is not csvfile...")
        print("")
        csvOpen()

    print(snd)
    if snd == True:
        print("Initial file make...")
        makeIni(csvFile)
        return csvfileDir
    else:
        print("")
        csvOpen()

# 第二処理
def csvFlasher(file):
    csv = file
    print(csv)


## main ##
str = csvOpen()
csvFlasher(str)
