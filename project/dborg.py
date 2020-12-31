#!/usr/bin/env python3
# -* coding: utf-8 -*-

from getopt import getopt, GetoptError
from sys import argv
from os import getcwd
import requests

from secrets import API_USERNAME, API_KEY

SCHEME = 'https://'
BASE_URL = 'www.screenscraper.fr/api2/'
BASE_PAYLOAD = { 'devid' : API_USERNAME , 'devpassword' : API_KEY, 'output' : 'json', 'softname' : 'dborg' }

short_opts = "hgaSs:n:u:p:b:"
long_opts = ["help", "name=", "getid", "get-all-media" "get-systems-list",
             "username=", "password=", "system-name="]

SYSTEMSLIST_DAT = 'dborg_systems_list.dat'

def usage():
    print("""
    Usage:
    ======

        --username <api user>   Set user for API calls
                                (-u <api user>)

        --password <api passwd> Set password for API user
                                (-p <api password>)

        --name <game name>      Set name of game which work with
                                (-n <game name>)

        --system-name <system>  Set system for game
                                (-s <system>)

        --basedir <directory>   Set target dir (create if not exists).
                                If not set, use: "./media"
                                (-b <directory>)

        --getid                 (returns 0 if exist)
                                (-g)

        --get-all-media         Get all media (logos, video, boxart, ...)
                                (-a)

        --get-systems-list      Get a list of systems available (dborg_systems_list.dat)
                                (-S)

        --help                  This help
                                (-h)

    Files created:
    ==============

    - dborg_systems_list.dat


""")

def apicall(apicmd, payload):
    url = SCHEME + BASE_URL + apicmd
    r = requests.get(url, params = payload)
    if r.status_code >= 400:
        r = None
    return r.status_code, r.json()

def get_gameid(gamename):
    return 0

def get_boxarts(basedir, gamename):
    pass

def get_video(basedir, gamename):
    pass

def get_logos(basedir, gamename):
    pass

def get_systems_list():
    apicmd = 'systemesListe.php'
    c, r = apicall(apicmd, BASE_PAYLOAD)
    if c >= 400:
        print('Error 400!')
        exit(1)
    systemes = []
    for systeme in r['response']['systemes']:
        systemes += [{'id': systeme['id'], 'name' : systeme['noms']['nom_eu']}]
    print(systemes)
    with open(SYSTEMSLIST_DAT, "w") as f:
        for systeme in sorted(systemes, key=lambda names: names['name']):
            f.write("%3d  :  %s\n" %(systeme['id'], systeme['name']))

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
    get_systems = False

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
        elif o in ("-a", "--get-all-media"):
            get_all = True
        elif o in ("-S", "--get-systems-list"):
            get_systems = True
        elif o in ("-s", "--system-name"):
            system_name = a
        elif o in ("-u", "--username"):
            BASE_PAYLOAD['devid'] = a
        elif o in ("-p", "--password"):
            BASE_PAYLOAD['devpassword'] = a
        else:
            assert False, "unhandled option"

    if get_systems:
        get_systems_list()
    elif get_id:
        if gamename:
            get_gameid(gamename)
    elif get_all:
        if base_dir == None:
            basedir = "%s/media" %getcwd()
        if gamename:
            get_all_media(basedir, gamename)

if __name__ == '__main__':
    main()

