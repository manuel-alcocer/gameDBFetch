#!/usr/bin/env python3
# -* coding: utf-8 -*-

from getopt import getopt, GetoptError
from sys import argv
from os import getcwd

import sqlite3

import requests

from secrets import API_USERNAME, API_KEY

from os.path import expanduser
HOME = expanduser("~")

SCHEME = 'https://'
BASE_URL = 'www.screenscraper.fr/api2/'
BASE_PAYLOAD = { 'devid' : API_USERNAME , 'devpassword' : API_KEY, 'output' : 'json', 'softname' : 'dborg' }

short_opts = "hgaSRs:n:u:p:b:"
long_opts = ["help", "name=", "getid", "get-all-media" "get-systems-list",
             "username=", "password=", "system-name=", "get-regions-list"]

PREFERRED_REGIONS = ( 'ss', 'wor', 'us', 'eu', 'jp' )

DB = HOME + '/.dborg.db'

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

        --get-systems-list      Get a list of systems available
                                (-S)

        --get-regions-list      Get a list of regions available
                                (-R)

        --help                  This help
                                (-h)

""")

def apicall(apicmd, payload):
    url = SCHEME + BASE_URL + apicmd
    r = requests.get(url, params = payload)
    if r.status_code >= 400:
        print('Error 400!')
        exit(1)
    return r.status_code, r.json()

def select_nom_region(jeu):
    region_matched = None
    for prefreg in PREFERRED_REGIONS:
        for nom in jeu['noms']:
            if nom['region'] == prefreg:
                return jeu['id'], nom['region'], nom['text']
    return jeu['id'], jeu['noms'][0]['region'], jeu['noms'][0]['text']

def select_jeu(jeux):
    choice = None
    for jeu in jeux:
        gameid, region, name = select_nom_region(jeu)
        print("%7d : %s (%s)" %(int(gameid), name, region))


def get_gameid(systemeid, recherche):
    apicmd = 'jeuRecherche.php'
    payload = BASE_PAYLOAD
    payload['recherche'] = recherche
    payload['systemeid'] = systemeid
    c, r = apicall(apicmd, payload)
    if len(r['response']['jeux'][0]) == 0:
        print("No game matched")
    else:
        jeux = r['response']['jeux']
        if len(jeux) > 1:
            jeu = select_jeu(jeux)
        else:
            gameid, region, name = select_nom_region(jeux[0])
            print("%7d : %s (%s)" %(int(gameid), name, region))
    return 0

def update_region_list():
    apicmd = 'regionsListe.php'
    payload = BASE_PAYLOAD
    conn = sqlite3.connect(DB)
    cnc = conn.cursor()
    c, r = apicall(apicmd, payload)
    for region in r['response']['regions']:
        reg = r['response']['regions'][region]
        reg_id = reg['id']
        reg_name = reg['nomcourt']
        if 'nom_en' in reg:
            reg_longname = reg['nom_en']
        elif 'nom_fr' in reg:
            reg_longname = reg['nom_fr']
        else:
            reg_longname = reg_name
        reg_parent = reg['parent']
        print("%s %s %s %s" %(reg_id, reg_name, reg_longname, reg_parent))
        cnc.execute('''INSERT INTO region
                        VALUES ('%s','%s','%s', '%s')'''
                    %(reg_id, reg_name, reg_longname, reg_parent))
        conn.commit()
    conn.close()

def get_boxarts(basedir, gamename):
    pass

def get_video(basedir, gamename):
    pass

def get_logos(basedir, gamename):
    pass

def get_systems_list():
    apicmd = 'systemesListe.php'
    c, r = apicall(apicmd, BASE_PAYLOAD)
    systemes = []
    for systeme in r['response']['systemes']:
        systemes += [{'id': systeme['id'], 'name' : systeme['noms']['nom_eu']}]

    with open(SYSTEMSLIST_DAT, "w") as f:
        for systeme in sorted(systemes, key=lambda names: names['name']):
            f.write("%3d  :  %s\n" %(systeme['id'], systeme['name']))
        print("File %s created" %SYSTEMSLIST_DAT)

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
    systemname = None
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
            systemname = a
        elif o in ("-u", "--username"):
            BASE_PAYLOAD['devid'] = a
        elif o in ("-p", "--password"):
            BASE_PAYLOAD['devpassword'] = a
        elif o in ("-R", "--get-regions-list"):
            update_region_list()
            exit(0)
        else:
            assert False, "unhandled option"

    if get_systems:
        get_systems_list()
    elif get_id:
        if gamename and systemname:
            get_gameid(systemname, gamename)
    elif get_all:
        if base_dir == None:
            basedir = "%s/media" %getcwd()
        if gamename:
            get_all_media(basedir, gamename)

if __name__ == '__main__':
    main()

