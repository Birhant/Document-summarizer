import os
import pickle
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from . import set
from ..code.reader import Read
from ..models import Process
from .validators import validate_file
from .doc_format import export_format
from .doc_format import export_format_0
from ..code.write_pdf import Write
from ..code.write_ppt import PPT

def name_doc_text(request, process, ext):
    media_root = settings.MEDIA_ROOT
    progress = process.progress
    process_type = process.process_type
    dir=f"processes\\{process_type}\\{request.user.username}"
    dir_root = f'{media_root}{dir}'
    filename = f"{progress}{ext}"
    file=os.path.join(dir_root,filename)
    url = file.replace(media_root, settings.MEDIA_URL)
    return file, url


def naming_file(request, file_type):
    file_types={'keyword':"multiple_documents"}
    file_name=''
    username=request.user.username
    file_name+=username+'_'
    file_name+=file_types[file_type]
    ext = '.txt'
    return file_name

def uploaded_multiple(request, path, files):
    file_name=naming_file(request, 'keyword')
    path=os.path.join(path,file_name)
    with open(path,'w')as writer:
        myfile = File(writer)
        for file in files:
            myfile.write(file)
            myfile.write('\n')
    return path

def save(request, uploaded_file, process_index):
    process_type = Process.process_type_choices[process_index][0]
    username = request.user.username
    media_root = settings.MEDIA_ROOT
    directory = f'processes\\{process_type}\\{username}'
    dir_root = os.path.join(media_root, directory)
    fs = FileSystemStorage(location=dir_root)
    name = fs.save(uploaded_file.name, uploaded_file)
    relative_path = os.path.join(directory,name)
    absolute_path = os.path.join(dir_root,name)
    return name, relative_path, dir_root

def reader(request, file_path):
    error = True
    read = Read(file_path)
    read.open()
    if read.status:
        read.convert()
        if read.status:
            error = False

    return error, read



def write(request, doc_text, process, ext='.pkl'):
    try:
        error = False
        if (ext == ".pkl"):
            path, _ = name_doc_text(request, process, ext)
            with open(path, 'wb') as writer:
                pickle.dump(doc_text, writer)
        else:
            path, _ = name_doc_text(request, process, ext)
            if(os.path.exists(path)):
                os.remove(path)
            with open(path, 'wb') as writer:
                writer.write(doc_text)
    except Exception:
        error = True
        messages.warning(request , f'Problem during writing text.')
    return error


def remove_files(file,index):
    dir = os.path.join(settings.MEDIA_ROOT, file.path)
    if (index == 1):
        with open(dir, 'r')as reader:
            files = reader.read()
        try:
            os.remove(dir)
            files = files.strip()
            files = files.split('\n')
            base, _ = os.path.split(dir)
            for file in files:
                path = os.path.join(base, file)
                os.remove(path)
        except Exception:
            a=10
    else:
        try:
            os.remove(dir)
        except Exception:
            a=10

def read(request, process, ext='.pkl'):
    error=False
    path, _ = name_doc_text(request, process, ext)
    try:
        if(ext=='.pkl'):
            with open(path,'rb')as reader:
                doc=pickle.load(reader)
        else:
            with open(path,'r')as reader:
                doc=reader.read(reader)
    except Exception:
        doc=None
        error = True
        messages.warning(request , f'Problem during reading file.')
    return error, doc

def prepare_text(doc_text):
    prepared_text = []
    text_under_heading = ''
    current_style=''
    for page_text in doc_text:
        for block_text in page_text:
            text = block_text[0]
            style = block_text[1]
            if style.startswith('heading'):
                content = (current_style,text_under_heading)
                prepared_text.append(content)
                text_under_heading = ''
                current_style = text, style
            else:
                text_under_heading +=text
    return prepared_text


def remove_related(request, process, process_index):
    for i in Process.progress_choices:
        process.progress=i[0]
        process.save()
        path, _=name_doc_text(request, process,'.pkl')
        try:
            os.remove(path)
        except Exception:
            error=True
    process.delete()
    return error

def export_fname(request, process, mode):
    exts = {'PDF':'.pdf','PPT':'.ppt'}
    ext = exts[mode]
    path, url = name_doc_text(request, process, ext)
    dir, fname = os.path.split(path)
    pdf = process.file.name
    _, pdf_name = os.path.split(pdf)
    pdf_name,_ = os.path.splitext(pdf_name)
    fname = str(pdf_name+"_"+fname)
    path = os.path.join(dir,fname)
    dir, _ = os.path.split(url)
    url = os.path.join(dir, fname)
    return path, url




def apply_export(request, doc_text, process, mode):
    error = False
    dir = ''

    write_format = export_format(doc_text)
    path, url = export_fname(request, process, mode)
    if mode=="PDF":
        pdf_write = Write()
        pdf_write.main(write_format)
        pdf_write.save(path)
    else:
        ppt_create=PPT()
        ppt_create.write(write_format)
        ppt_create.save(path)

    return error, url

def apply_export_multiple(request, doc_text, process, mode):
    error = False
    dir = ''

    write_format = export_format_0(doc_text)
    path, url = export_fname(request, process, mode)
    if mode=="PDF":
        pdf_write = Write()
        pdf_write.main(write_format)
        pdf_write.save(path)
    else:
        print(write_format)
        ppt_create=PPT()
        ppt_create.write(write_format)
        ppt_create.save(path)

    return error, url


def get_files(request):
    files = []
    process = set.process_all_db(request,1)
    path=process.file.path
    dir,_ = os.path.split(path)
    with open(path, 'r')as reader:
        files=reader.read()
        files=files.strip()
        files=files.split('\n')
    return files


def save_file(request, uploaded_files, process_index):
    files = []
    error = False
    for uploaded_file in uploaded_files:
        status = validate_file(request, uploaded_file)
        if status:
            name, relative_path, dir_root = save(request, uploaded_file, process_index)
            files.append(name)
    if process_index == 1:
        file_name = uploaded_multiple(request, dir_root, files)
    else:
        file_name = relative_path
    error = set.save_process(request, file_name, process_index)

    return error


