import os
from django.contrib import messages
from django.core.exceptions import ValidationError

def validate_file(request, value):
    status=False
    path=str(value)
    valid_types=[".pdf", ".epub"]
    _, base = os.path.split(path)
    name, ext = os.path.splitext(base)
    if(ext in valid_types):
        status = True
    else:
        messages.warning(request, f'Your file should be pdf')
    return status

def validate_page_range(request, start, end):
    error=False
    start = int(start)
    if end !="None":
        end = int(end)
    else:
        end = -1
    if(start>=end and end != -1):
        error = True
        start = None
        end   = None
        messages.warning(request, f'starting page should be smaller than ending page')
    return error, start, end

