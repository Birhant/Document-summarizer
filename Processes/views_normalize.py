from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from .views import catch_error
from .forms import UploadFileForm
from .supporters import get
from .supporters import set
from .supporters import logics
from .supporters import actions

##pdf normalizer
@login_required
@catch_error
def upload_broken_book(request):
    error=False
    process_index = 2
    progress_index = 0
    form = UploadFileForm()
    completed=False
    process= get.process_all_db(request, process_index)
    if process is not None:
        completed = True
        set.update_process(request, process_index, progress_index, 0)
    else:
        error, completed = logics.upload(request, UploadFileForm, process_index)

    title = "Upload"
    context={'title' : title, 'form' : form, 'completed' : completed, 'error' : error}
    return render(request, "Process/PDFNormalizer/upload.html", context)

@login_required
@catch_error
def read_broken_book(request, *args, **kwargs):
    process_index = 2
    progress_index = 1
    process = get.process_all_db(request,process_index)
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("UploadBrokenBook")
    error, read, completed , password = logics.decrypt_file_logic(request, process_index)
    if completed:
        error, process = set.update_process(request, process_index, progress_index, 0)
        return redirect('GenerateToCBook',password=password)
    context={'error': error, 'completed': completed}
    return render(request, "Process/PDFNormalizer/read.html", context)



@login_required
@catch_error
def correct_broken_book(request, password):
    process_index = 2
    progress_index = 2
    completed =False
    error = False
    toc = []
    error, completed = logics.generate_toc(request, password)
    if completed:
        return redirect("ViewToCBook")
    title = "generate_toc"
    context={'title' : title, 'toc' : toc, 'completed' : completed, 'error' : error}
    return render(request, "Process/PDFNormalizer/upload.html", context)

@login_required
@catch_error
def view_toc(request):
    process_index = 2
    progress_index = 2
    error, completed, unique_toc = logics.select_toc(request, process_index, progress_index)
    if completed:
        return redirect('ExportBrokenBook')
    title = "view_toc"
    context={'title' : title, 'toc' : unique_toc, 'completed' : completed, 'error' : error}
    return render(request, "Process/PDFNormalizer/toc_list.html", context)

@login_required
@catch_error
def export_broken_book(request):
    process_index = 2
    progress_index = 5
    valid = logics.check_stage(request, process_index, 2)
    if not valid:
        return redirect("ReadBrokenBook")
    error, completed, url = logics.export_broken(request)
    title="Export book"
    context={'title':title, 'error': error, 'url':url, 'completed': completed}
    return render(request, "Process/PDFNormalizer/export.html", context)

@login_required
@catch_error
def remove_broken_book(request):
    process_index = 2
    error = logics.remove_logic(request, process_index)
    if not error:
        return redirect('UploadBrokenBook')
    else:
        return redirect('Home')
