from django.db import models
from .validators import validate_one_row, validate_file_is_dir
from django.core.files.storage import FileSystemStorage

def hide_password(string):
    ret_char = ''
    for char in string:
        ret_char+='*'
    return ret_char

# Create your models here.
class Region(models.Model):
    id_region = models.IntegerField(unique = True)
    name = models.CharField(max_length = 4, unique = True)
    longname = models.CharField(max_length = 50)

class System(models.Model):
    id_system = models.IntegerField(unique = True)
    name = models.CharField(max_length = 255, unique = True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class SystemExtension(models.Model):
    extension = models.CharField(max_length = 255)
    system = models.ManyToManyField(System)

    def __str__(self):
        return self.extension

    def system_ext(self):
        return '.'.join([str(p) for p in self.system.all() ])
    system_ext.short_description = 'System'

class Game(models.Model):
    id_game = models.IntegerField(unique = True)
    name = models.CharField(max_length = 255, unique = True)
    region = models.ForeignKey(Region, to_field = 'name', on_delete=models.DO_NOTHING)
    system = models.ForeignKey(System, to_field = 'name', on_delete=models.DO_NOTHING)

class Table(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class TableUpdate(models.Model):
    name = models.ForeignKey(Table, to_field = 'name', on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.name

class ExtApidata(models.Model):
    name     = models.CharField(max_length = 255, unique = True)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    base_url = models.URLField(max_length = 200)
    api_base = models.CharField(max_length = 255)
    output   = models.CharField(max_length = 255)
    softname = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

    def password_hidden(self):
        return hide_password(self.password)


class Config(models.Model):
    storage = FileSystemStorage()
    id_config = models.IntegerField(primary_key = True, validators = [validate_one_row])
    name = models.ForeignKey(ExtApidata, to_field = 'name', on_delete=models.CASCADE)
    games_base_dir = models.CharField(max_length=1024, validators = [validate_file_is_dir], default = storage.location)
    games_target_base_dir = models.CharField(max_length=1024, validators = [validate_file_is_dir], default = storage.location)

    def __str__(self):
        return self.name.name

def get_games_base_dir():
    return Config.objects.all()[0].games_base_dir

def get_system_extension():
    return '(' + '|'.join([ e['extension'] for e in SystemExtension.objects.values('extension').distinct()[::] ]) + ')$'

class LocalGameFile(models.Model):
    filename = models.FilePathField(path = get_games_base_dir(), recursive=True, match = get_system_extension())
    crc = models.CharField(max_length = 16)

    def __str__(self):
        return self.filename
