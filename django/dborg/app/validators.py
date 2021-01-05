from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from os import path

def validate_one_row(value):
    if value != 1:
        raise ValidationError(
            _('%(value)s is not 1'),
            params = { 'value' : value },
        )

def validate_file_is_dir(value):
    if not path.isdir(value):
        raise ValidationError(
        _('%(value)s is not a directory'),
        params = { 'value' : value },
        )
