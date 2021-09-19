import os
from ..models import PickledModel
from django.core.exceptions import ValidationError
import re

def validate_file(value):
    status=False
    path=str(value)
    valid_types=[".pkl", ".pk", ".py"]
    _, base = os.path.split(path)
    name, ext = os.path.splitext(base)
    if(ext in valid_types):
        status = True
    return status

def validate_name(value):
    models=PickledModel.objects.filter(name=value)
    model=models.values()
    if len(model)>0:
        status=False
    else:
        status=True
    return status

