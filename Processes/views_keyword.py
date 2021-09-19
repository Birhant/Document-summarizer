from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import UploadMultipleFileForm
from .forms import SearchFileForm
from .supporters import get
from .supporters import set
from .supporters import logics
from .supporters import actions
from .views import catch_error
##keywordbased summarizer
@login_required
@catch_error
def upload_multiple_book(request):
    error=False
    process_index = 1
    progress_index = 0
    form = UploadMultipleFileForm()
    completed=False
    process= get.process_all_db(request, process_index)
    if process is not None:
        completed = True
    else:
        error, completed = logics.upload(request, UploadMultipleFileForm, process_index)

    title = "Upload"
    context={'title' : title, 'form' : form, 'completed' : completed, 'error' : error}
    return render(request, "Process/KeywordSummarizer/upload.html", context)

@login_required
@catch_error
def read_multiple_book(request, *args, **kwargs):
    process_index = 1
    progress_index = 1
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("UploadMultipleBook")
    form = SearchFileForm
    error, completed = logics.read_multiple_logic(request, process_index, progress_index, form)
    if completed:
        return redirect('SummarizeMultipleBook')
    context={'error': error, 'form':form, 'completed': completed}
    return render(request, "Process/KeywordSummarizer/read.html", context)

@login_required
@catch_error
def summarize_multiple_book(request):
    process_index = 1
    progress_index = 2
    error = completed = False
    headings = []
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("ReadMultipleBook")
    error, summarizers, completed = logics.multiple_summary(request)
    title="Summarizer"
    context={'title':title,'error': error, 'summarizers':summarizers, 'completed': completed}
    return render(request, "Process/KeywordSummarizer/summarize.html", context)

@login_required
@catch_error
def export_multiple_book(request):
    process_index = 1
    progress_index = 5
    valid = logics.check_stage(request, process_index, progress_index-3)
    if not valid:
        return redirect("SummarizeMultipleBook")
    error, url, completed = logics.export_logic_multiple(request, process_index, progress_index)
    title="Export book"
    context={'title':title, 'error': error, 'url':url, 'completed': completed}
    return render(request, "Process/KeywordSummarizer/export.html", context)

@login_required
@catch_error
def remove_multiple_book(request):
    try:
        process_index = 1
        error = logics.remove_logic(request, process_index)
        if not error:
            return redirect('UploadMultipleBook')
    except Exception:
        return redirect('Home')

