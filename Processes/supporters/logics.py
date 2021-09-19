import os
from django.conf import settings
from django.contrib import messages
from ..models import Process
from . import actions
from . import code_logic
from . import get
from . import set
from . import code_logic
from .validators import validate_file
from ..code.get_content import Content
from ..code.get_content import correct_toc

from Summarizers.supporters import get as get_summarizer

def check_stage(request, process_index, requirement):
    valid = False
    process = get.process_all_db(request, process_index)
    if process is not None:
        current = process.progress
        element = (current ,current)
        progress_index=Process.progress_choices.index(element)
        if progress_index>=requirement:
            valid = True
        set.update_process(request, process_index, requirement, 0)
    return valid

def upload(request, uploadform, process_index):
    error = False
    completed = False
    files = []
    if request.method=="POST":
        form = uploadform(request.POST, request.FILES)
        if process_index == 1:
            uploaded_files = request.FILES.getlist('file')
        else:
            uploaded_files=[request.FILES['file']]
        if form.is_valid():
            error = actions.save_file(request, uploaded_files, process_index)
            if not error:
                completed = True
    return error, completed


def decrypt(request, read):
    error = False
    password = request.POST.get('password')
    status = read.decrypt(password)
    if not status:
        error = True
        messages.warning(request, f"Incorrect password")
    return error, read, password


def decrypt_file_logic(request, process_index):
    completed = False
    password = False
    _, file_path = get.uploaded_file_path(request, process_index)
    error, read = actions.reader(request, file_path)
    if not error:
        if read.encrypted:
            messages.warning(request, "We do not support encrypted file")
            password = True
        else:
            completed = True
    else:
        messages.warning(request, "Cannot read uploaded file")

    return error, read, completed , password

def read_file_logic(request, password, process_index):
    process, file_path = get.uploaded_file_path(request, process_index)
    if file_path is not None:
        error, read = actions.reader(request, file_path)
        if not error:
            if read.encrypted:
                error = True
    return error, read, process

def extract_logic(request, password, process_index, progress_index):
    completed = False
    error, read, process = read_file_logic(request, password, process_index)
    if not error:
        error, completed, headings = code_logic.code_extract(request, read, process_index, progress_index)
    return error, read, headings, completed

def headings_logic(request, process_index, progress_index):
    heading_toc = []
    process = get.process_all_db(request, process_index)
    error, values = actions.read(request, process, '.pkl')
    if len(values)!=4:
        error, process  = set.update_process(request, process_index, progress_index ,-1)
        error, values = actions.read(request, process, '.pkl')

    if not error:
        error, completed, heading_toc = code_logic.code_headings(request, values, process_index, progress_index)
    return error, completed, heading_toc

def summary_logic(request, process_index, progress_index):
    completed = False
    summarizers = get_summarizer.all_summarizers_name()
    error, process = set.update_process(request, process_index, progress_index, -1)
    error,doc_text = actions.read(request, process, '.pkl')
    if(request.method=="POST"):
        summarizer_name=request.POST['summarizer']
        error, completed = code_logic.code_summarize(request, doc_text, summarizer_name, process_index, progress_index)
    return error, summarizers, completed

def export_logic(request, process_index, progress_index):
    error = False
    completed = False
    path = ''
    if request.method=='POST':
        mode = request.POST.get('mode')
        process = get.process_all_db(request, process_index)
        error,doc_text = actions.read(request, process, '.pkl')
        process.progress = Process.progress_choices[progress_index][0]
        error, path = actions.apply_export(request, doc_text, process, mode)
        if not error:
            completed = True
    return error, path, completed


def export_logic_multiple(request, process_index, progress_index):
    error = False
    completed = False
    path = ''
    if request.method=='POST':
        mode = request.POST.get('mode')
        process = get.process_all_db(request, process_index)
        error,doc_text = actions.read(request, process, '.pkl')
        process.progress = Process.progress_choices[progress_index][0]
        error, path = actions.apply_export_multiple(request, doc_text, process, mode)
        if not error:
            completed = True
    return error, path, completed

def remove_logic(request, process_index):
    error = False
    process = get.process_all_db(request, process_index)
    if process is not None:
        file=process.file
        actions.remove_files(file, process_index)
        actions.remove_related(request, process, process_index)
    else:
        messages.warning(request, f"Error while deleting process")
        error=True
    return error

def read_multiple(request, process_index, path):
    completed = False
    error = False
    error, read = actions.reader(request, path)
    if not error:
        if read.encrypted:
            error = True
            messages.warning(request, f'Password protected files are not supported for keyword based summarizer.')
    else:
        completed = True
    return completed, read


def read_multiple_logic(request, process_index, progress_index, readform):
    completed = False
    error = False
    files = actions.get_files(request)
    if(request.method=='POST'):
        form = readform(request.POST, request.FILES)
        if(form.is_valid()):
            data = form.cleaned_data
            search = data['search']
            cont=Content(search)
            process = get.process_all_db(request,process_index)
            path=process.file.path
            dir,_ = os.path.split(path)
            for file in files:
                path = os.path.join(dir, file)
                path = os.path.join(settings.MEDIA_ROOT,path)
                error, read = read_multiple(request, process_index, path)
                if not error:
                    cont.get_content(read.doc)
        if cont.doc_text is None:
            error = True
            messages.warning(request, f"No related content found.")            
        if not error:
            error, process = set.update_process(request, process_index, progress_index, 0)
            error = actions.write(request, cont.doc_text, process, ext='.pkl')
            completed = True
        else:
            messages.warning(request, f"The documents have no related content")
    return error, completed


def multiple_summary(request):
    process_index = 1
    progress_index = 2
    completed = False
    summarizers = get_summarizer.all_summarizers_name()
    process = get.process_all_db(request, process_index)
    error,doc_text = actions.read(request, process, '.pkl')
    if(request.method=="POST"):
        summarizer_name=request.POST['summarizer']
        error, summary =code_logic.multiple_summarize(request, doc_text, None, 3, summarizer_name)
        if not error:
            error, process = set.update_process(request, process_index, progress_index, 0)
            if not error:
                error = actions.write(request, summary,process,ext='.pkl')
                if not error:
                    completed=True
        
    return error, summarizers, completed

def generate_toc(request, password):
    process_index = 2
    progress_index = 2
    completed = False
    error, read, process = read_file_logic(request, password, process_index)
    if not error:
        toc = correct_toc(read.doc)
        error, process = set.update_process(request, process_index, progress_index, 0)
        actions.write(request, toc, process, ext='.pkl')
        completed = True
    return error, completed

def select_toc(request, process_index, progress_index):
    error = False
    completed = False
    toc = []
    unique_toc = []
    error, process = set.update_process(request, process_index, progress_index, 0)
    if process is not None:
        error,toc = actions.read(request, process, '.pkl')
    index = 0
    for i in toc:
        lvls = [j[0] for j in unique_toc]
        if i[0] not in lvls:
            i = list(i)
            i.append(index)
            index+=1
            unique_toc.append(i)
    if request.method=="POST":
        for i,heading in enumerate(unique_toc.copy()):
            name = 'heading_'+str(heading[3])
            value = request.POST.get(name)
            if value != "None":
                lvl = int(value)
                unique_toc[i][0] = lvl
        current = 0
        threshold = 0
        for i, heading in enumerate(toc.copy()):
            if(heading == unique_toc[current]):
                toc[i] = unique_toc[current]
                current +=1
            if i==0:
                threshold = heading[0]
            if heading[0] == threshold:
                toc[i][0] = 1
            elif heading[0] > threshold:
                toc[i][0] = 2
            else:
                toc[i][0] = 1
        error = actions.write(request, toc, process, ext='.pkl')
        if not error:
            completed = True
    return error, completed, unique_toc

def export_broken(request):
    completed = False
    url = ''
    process_index = 2
    progress_index = 7
    error, process = set.update_process(request, process_index, progress_index, -5)
    if not error:
        error, read, process = read_file_logic(request, '', process_index)
        error,toc = actions.read(request, process, '.pkl')
        read.doc.setToC(toc)
        try:
            error, process = set.update_process(request, process_index, progress_index, 0)
            path, url = actions.name_doc_text(request, process, '.pdf')
            read.doc.save(path)
            completed = True
        except Exception:
            error = True
    return error, completed, url
