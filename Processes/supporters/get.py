import os
from django.conf import settings
from django.contrib import messages
from ..models import Process

def process_all_db(request, process_index):
    process_type = Process.process_type_choices
    try:
        process = Process.objects.get(actor=request.user, \
                                         process_type = process_type[process_index][0], 
                                         )
    except Exception:
        process=None
    return process

def process_db(request, process_index, progress_index=0):
    process_type = Process.process_type_choices
    progress_stage = Process.progress_choices
    try:
        process = Process.objects.get(actor=request.user, \
                                         process_type = process_type[process_index][0], 
                                         progress = progress_stage [progress_index][0]\
                                         )
    except Exception:
        process=None
    return process

def process_filter(request, process_index):
    process_type = Process.process_type_choices[process_index][0]
    process = Process.objects.filter(actor=request.user, \
                                        process_type = process_type, \
                                        )
    return process, process_type

def filter_book_summarizer(request, progress_index):
    process = process_filter(request, 0)
    process_type=Process.process_type_choices[0][0]
    new_process = process.filter(progress=progress_index)
    new_process = new_process.values()
    return new_process, process_type

def uploaded_file_path(request, process_index):
    process = process_all_db(request, process_index)
    path = None
    if process is not None:
        file = process.file
        path = os.path.join(settings.MEDIA_ROOT,file.path)
    return process, path
