from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UploadFileForm
from .supporters import set
from .supporters import get
from .supporters import logics
from .supporters import actions

def catch_error(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            messages.warning(args[0],"error occured")
            return redirect('Home')
    return inner_function


# Create your views here.
@login_required
@catch_error
def upload_single_book(request):
    error=False
    process_index = 0
    progress_index = 0
    form = UploadFileForm()
    completed=False
    process = get.process_all_db(request, process_index)
    if process is not None:
        completed = True
    else:
        error, completed = logics.upload(request, UploadFileForm, process_index)
    title = "Upload"
    context={'title' : title, 'form' : form, 'completed' : completed, 'error' : error}
    return render(request, "Process/BookSummarizer/upload.html", context)

@login_required
@catch_error
def read_single_book(request, *args, **kwargs):
    process_index = 0
    progress_index = 1
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("UploadSingleBook")
    error, read, completed , password = logics.decrypt_file_logic(request, process_index)
    if password:
        return redirect('RemoveSingleBook')
    if completed:
        error, process = set.update_process(request, process_index, progress_index, 0)
        return redirect('ExtractSingleBook',password=password)
    title = "Read PDF"
    context={'title' : title, 'error': error, 'completed': completed}
    return render(request, "Process/BookSummarizer/read.html", context)


@login_required
@catch_error
def extract_single_book(request, password, **kwargs):
    process_index = 0
    progress_index = 2
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("ReadSingleBook")
    error, read ,headings, completed= logics.extract_logic(request, password, process_index, progress_index)
    if completed:
        set.update_process(request, process_index, progress_index, 0)
        return redirect("HeadingSingleBook")
    if headings==[]:
        messages.warning(request,"You need to generate table of content in order to summarize your text.")
        return redirect("UploadBrokenBook")

    title="Extract"
    context={'title':title,'error': error, 'headings':headings, 'completed': completed}
    return render(request, "Process/BookSummarizer/extract.html", context)


@login_required
@catch_error
def headings_single_book(request):
    process_index = 0
    progress_index = 3
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("ReadSingleBook")
    error, completed, heading_toc = logics.headings_logic(request, process_index, progress_index)
    if completed:
        set.update_process(request, process_index, progress_index, 0)
    title="Get Heading text"
    context={'title':title,'error': error, 'headings':heading_toc, 'completed': completed}
    return render(request, "Process/BookSummarizer/headings_text.html", context)


@login_required
@catch_error
def summarize_single_book(request):
    process_index = 0
    progress_index = 4
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("HeadingSingleBook")
    error, summarizers, completed = logics.summary_logic(request, process_index, progress_index)
    if completed:
        set.update_process(request, process_index, progress_index, 0)
    title="Summarize book"
    context={'title':title, 'error': error, 'summarizers':summarizers, 'completed': completed}
    return render(request, "Process/BookSummarizer/summarizers.html", context)


@login_required
@catch_error
def export_single_book(request):
    process_index = 0
    progress_index = 5
    valid = logics.check_stage(request, process_index, progress_index-1)
    if not valid:
        return redirect("SummarizeSingleBook")
    error, url, completed = logics.export_logic(request, process_index, progress_index)
    if completed:
        set.update_process(request, process_index, progress_index, 0)
    title="Export book"
    context={'title':title, 'error': error, 'download':url, 'completed': completed}
    return render(request, "Process/BookSummarizer/export.html", context)


@login_required
@catch_error
def remove_single_book(request):
    process_index = 0
    error = logics.remove_logic(request, process_index)
    if not error:
        return redirect('UploadSingleBook')
    else:
        return redirect('Home')

