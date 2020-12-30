#!/usr/bin/env python3
# -* coding: utf-8 -*-

from getopt import getopt, GetoptError
from sys import argv
from os import getcwd

API_KEY='Hackme.1234'
API_USERNAME='AssButt'

short_opts = "hgan:"
long_opts = ["help", "name=", "getid", "get-all"]

def usage():
    print("""
    Usage:
    ======

        --name <game name>      Set name of game which work with
                                (-n <game name>)

        --getid                 (returns 0 if exist)
                                (-g)

        --basedir <directory>   Set target dir (create if not exists).
                                If not set, use: "./media"
                                (-b <directory>)

        --get-all               Get all media (logos, video, boxart, ...)
                                (-a)

        --help                  This help
                                (-h)

""")

def get_gameid(gamename):
    return 0

def get_boxarts(basedir, gamename):
    pass

def get_video(basedir, gamename):
    pass

def get_logos(basedir, gamename):
    pass

def get_all_media(basedir, gamename):
    print("Target dir: %s" %basedir)
    get_boxarts(basedir, gamename)
    get_video(basedir, gamename)
    get_logos(basedir, gamename)

    return 0

def main():
    try:
        opts, args = getopt(argv[1:], short_opts, long_opts)
    except GetoptError as err:
        print(err)
        usage()
        exit(2)

    gamename = None
    get_id = False
    base_dir = None
    get_all = False

    for o, a in opts:
        if o in ("-g", "--getid"):
            get_id = True
        elif o in ("-h", "--help"):
            usage()
            exit()
        elif o in ("-n", "--name"):
            gamename = a
        elif o in ("-b", "--basedir"):
            basedir = a
        elif o in ("-a", "--get-all"):
            get_all = True
        else:
            assert False, "unhandled option"

    if get_id:
        if gamename:
            get_gameid(gamename)
    elif get_all:
        if base_dir == None:
            basedir = "%s/media" %getcwd()
        if gamename:
            get_all_media(basedir, gamename)

if __name__ == '__main__':
    main()

