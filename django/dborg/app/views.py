from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render, redirect

from .models import Region, ExtApidata, TableUpdate, Config, Table, System

import datetime

from .core import get_region_list, get_system_list, update_regions, update_systems
from .core import scanfiles_for_system


NAVBAR = { 'active' : 'Home',
            'elements' : [
                { 'title' : 'Home', 'view' : 'app:index' },
                { 'title' : 'Games', 'view' : 'app:index' },
                { 'title' : 'Regions', 'view' : 'app:regions' },
                { 'title' : 'Systems', 'view' : 'app:systems' },
                { 'title' : 'Scan', 'view' : 'app:scan' },
            ]
        }

def index(request):
    navbar = NAVBAR
    navbar['active'] = 'Home'
    template = loader.get_template('app/index.html')
    result = TableUpdate.objects.order_by('-last_update').filter(name='Region')[:1]
    if len(result) == 0:
        regions_last_update = 'Never'
    else:
        regions_last_update = result[0].last_update.strftime("%Y-%m-%d %H:%M:%S")
    result = TableUpdate.objects.order_by('-last_update').filter(name='System')[:1]
    if len(result) == 0:
        systems_last_update = 'Never'
    else:
        systems_last_update = result[0].last_update.strftime("%Y-%m-%d %H:%M:%S")
    context = { 'active' : 'Home', 'reg_last_update' : regions_last_update , 'sys_last_update' : systems_last_update , 'navbar' : NAVBAR }
    return HttpResponse(template.render(context, request))

def regions(request):
    navbar = NAVBAR
    navbar['active'] = 'Regions'
    r_list = Region.objects.all()
    context = { 'region_list' : r_list , 'navbar' : navbar }
    return render(request, 'app/regions.html', context)

def systems(request):
    navbar = NAVBAR
    navbar['active'] = 'Systems'
    r_list = System.objects.all()
    context = { 'system_list' : r_list , 'navbar' : navbar }
    return render(request, 'app/systems.html', context)

def scan(request):
    navbar = NAVBAR
    navbar['active'] = 'Scan'
    system_list = [ system.name for system in System.objects.all() ]
    context = { 'navbar' : navbar , 'system_list' : system_list }
    return render(request, 'app/scan.html', context)

def addFiles(request, context):
    navbar = NAVBAR
    navbar['active'] = 'Scan'
    context['navbar'] = navbar
    return render(request, 'app/addfiles.html', context)

def actions(request):
    if request.method == 'POST':
        try:
            action = request.POST['action']
        except KeyError:
            return HttpResponse("Key not exists")

        if action == 'Update regions':
            if update_regions():
                return redirect('app:regions')
        elif action == 'Update systems':
            if update_systems():
                return redirect('app:systems')
        elif action == 'Scan system':
            file_list = scanfiles_for_system(request.POST['system'])
            context = { 'file_list' : file_list }
            response = addFiles(request, context)
            if len(file_list) > 0:
                return response

