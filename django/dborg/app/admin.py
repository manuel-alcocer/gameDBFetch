# Register your models here.
from django.contrib import admin

from .models import Region, System, Game, Table, TableUpdate, ExtApidata, Config, SystemExtension
from .models import LocalGameFile

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id_region', 'name', 'longname')

class SystemAdmin(admin.ModelAdmin):
    list_display = ('id_system', 'name')

class ApiExtdataAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'password_hidden', 'base_url', 'api_base')

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'games_base_dir', 'games_target_base_dir')

class SystemExtensionAdmin(admin.ModelAdmin):
    list_display = ('system_ext', 'extension')

admin.site.register(Region, RegionAdmin)
admin.site.register(System, SystemAdmin)
admin.site.register(Game)
admin.site.register(Table)
admin.site.register(TableUpdate)
admin.site.register(ExtApidata, ApiExtdataAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(SystemExtension, SystemExtensionAdmin)
admin.site.register(LocalGameFile)
