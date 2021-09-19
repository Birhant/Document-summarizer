from Summarizers.supporters.get import preprocessor
from django.contrib import messages
from . import validators
from .actions import insert_model
from ..models import PickledModel

def upload(request, data, preprocessor, message):
    completed = False
    status = validators.validate_file(data['file'])
    status = status or data['default']
    if status:
        error=insert_model(request, data, preprocessor)
        if not error:
            completed=True
        else:
            messages.warning(request, message)
    else:
        messages.warning(request, message)
    return completed

def upload_model_logic(request, form):
    completed=False

    if form.is_valid():
        data = form.cleaned_data
        status = validators.validate_name(data['name'])
        if status:
            preprocessor = request.POST.get("preprocessor")
            if not data['default']:
                if data['file'] is not None:
                    completed = upload(request, data, preprocessor, r'The file should be pickle')
                else:
                    messages.warning(request, r'The file should be pickle')
            else:
                completed = upload(request, data, preprocessor, 'message')
        else:
            messages.warning(request, r'The name should be unique')
    return completed
