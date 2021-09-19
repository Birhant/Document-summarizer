from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
from ..models import PickledModel
from . import get

def insert_model(request, data, preprocessor):
    error=False

    #Attributes
    media_root = settings.MEDIA_ROOT
    uploaded_file = data['file']
    name = data['name']
    purpose = data['purpose']
    default = data['default']
    preprocessor = preprocessor
    accuracy = data['accuracy']

    #File name
    directory=f'Models/{purpose}'
    dir_root = f'{media_root}{directory}'
    try:
        if(uploaded_file is not None):
            fs = FileSystemStorage(location=dir_root)
            fname = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file=directory+'/'+fname
            PickledModel.objects.create(name=name, file=uploaded_file, purpose=purpose,\
                                        preprocessor=preprocessor, accuracy=accuracy, \
                                        uploaded_by=request.user, default=default, slug="Models")
        else:
            uploaded_file=None
            PickledModel.objects.create(name=name, purpose=purpose,\
                                        preprocessor=preprocessor, accuracy=accuracy, \
                                        uploaded_by=request.user, default=default, slug="Models")
    except Exception:
        messages.warning(request, f"Error while saving the model to database")
        error=True
    return error


def summarize_simple(request, input, summarizer_name):
    output=''
    error, preprocessor, summarizer=get.summarizer(request, summarizer_name)
    if not error:
        if preprocessor is not None:
            try:
                error, processed = preprocessor(input)
            except Exception:
                error = True
                messages.warning(request, "Error while cleaning text")

        else:
            processed = input
        if not error:
            try:
                output = summarizer(processed)
            except Exception:
                error = True
        else:
            error = True
    else:
        output = input
    return error, output
