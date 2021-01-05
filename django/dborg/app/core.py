from .models import Config, System, Region, TableUpdate, Table
from .models import SystemExtension

import requests

from os import path, walk

def get_region_list(url, payload):
    r = requests.get(url, payload)
    if r.status_code >= 400:
        return [ r.status_code ]
    reg_list = [ r.status_code ]
    r = r.json()
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

        reg_list += [ { 'id' : reg_id, 'name' : reg_name,
                      'longname' : reg_longname, 'parent' : reg_parent } ]
    return reg_list

def get_system_list(url, payload):
    r = requests.get(url, payload)
    if r.status_code >= 400:
        return [ r.status_code ]
    systemes = [ r.status_code ]
    r = r.json()
    for systeme in r['response']['systemes']:
        systemes += [{'id': systeme['id'], 'name' : systeme['noms']['nom_eu']}]
    return systemes

def update_regions():
    r = Config.objects.get(id_config=1).name

    payload = { 'devid' : r.username, 'devpassword' : r.password,
               'output' : r.output, 'softname' : r.softname }
    url = r.base_url + '/' + r.api_base + '/regionsListe.php'
    reg_list = get_region_list(url, payload)

    if reg_list[0] == 200:
        for region in reg_list[1:]:
            obj, created = Region.objects.update_or_create(
                id_region = region['id'],
                name = region['name'],
                longname = region['longname']
            )
        TableUpdate.objects.create(name = Table.objects.get(name='Region'))
    return True

def update_systems():
    r = Config.objects.get(id_config=1).name

    payload = { 'devid' : r.username, 'devpassword' : r.password,
               'output' : r.output, 'softname' : r.softname }
    url = r.base_url + '/' + r.api_base + '/systemesListe.php'
    sys_list = get_system_list(url, payload)

    if sys_list[0] == 200:
        for system in sys_list[1:]:
            obj, created = System.objects.update_or_create(
                id_system = system['id'],
                name = system['name'],
            )
        TableUpdate.objects.create(name = Table.objects.get(name='System'))
    return True

def check_extension(ext_list, filename):
    for extension in ext_list:
        if extension == filename[len(filename) - len(extension):]:
            return True

def scanfiles_for_system(system):
    ext_list = [ c.extension for c in SystemExtension.objects.filter(system__name=system) ]
    games_base_dir = Config.objects.all()[0].games_base_dir

    ret_list = []

    for r, d, fl in walk(games_base_dir):
        for fn in fl:
            if check_extension(ext_list, fn):
                fullpath = path.join(r, fn)
                ret_list += [ [r, fn, fullpath] ]
    return ret_list

