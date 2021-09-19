from ..models import Process
from .get import process_db,process_all_db

def save_process(request, file_name, process_index, progress_index=0):
    process_type = Process.process_type_choices[process_index][0]
    progress = Process.progress_choices[progress_index][0]
    error = False
    try:
        Process.objects.create(actor=request.user, \
                                process_type=process_type, \
                                file=file_name, \
                                progress=progress,
                                )
    except Exception:
        error = True
    return error

def update_process(request, process_index, progress_index, step):
    error = True
    process = process_all_db(request, process_index)
    if process is not None:
        process.progress = Process.progress_choices[progress_index+step][0]
        process.save()
        error = False
    return error, process




