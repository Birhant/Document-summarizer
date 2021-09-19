from . import validators
from django.contrib import messages
from . import set
from . import get
from . import actions
from ..models import Process
from . import doc_format
from ..code.extract import Extract
from ..code.getHeadings import Headings
from Summarizers.supporters.actions import summarize_simple
from Summarizers.supporters import get as get_summarizer
def do_nothing(value):
    return value

def multiple_summarize(request, doc_text, prepare_style, summarize_style, summarizer_name,):
    formats = [ doc_format.prepare_format_0, doc_format.summary_format_0, None, doc_format.summary_format_1]
    if prepare_style is None:
        apply_prepare= do_nothing
    else:
        apply_prepare = formats[prepare_style]
    apply_summarize = formats[summarize_style]
    process_index   =1
    progress_index  =2
    completed = False
    summary = []
    prepared_text = apply_prepare(doc_text)
    for page in prepared_text:
        text = ' '.join(page)
        text = text.strip()
        error, summarized = summarize_simple(request, text, summarizer_name)
        if not error:
            summary.append(summarized)
    if summary == '':
        error = True
    else:
        error = False
    return error, summary


def code_summarize(request, doc_text, summarizer_name, process_index, progress_index):
    completed = False
    error = False
    summary = []
    prepared_text = actions.prepare_text(doc_text)
    prepared_text = prepared_text[1:]
    for heading, text in prepared_text:
        error, summarized = summarize_simple(request, text, summarizer_name)
        if not error:
            summary.append((heading,summarized))
    if summary != []:
        error, process = set.update_process(request, process_index, progress_index, 0)
        if not error:
            error = actions.write(request,summary,process,ext='.pkl')
            if not error:
                completed=True
    return error, completed

def code_headings(request, values, process_index, progress_index):
    completed = False
    error = False
    headings = Headings(request, *values)
    error, heading_para = headings.main()
    heading_toc = headings.heading_identified
    if not error:
        error, process = set.update_process(request, process_index, progress_index ,0)
        if not error:
            error = actions.write(request,heading_para,process,ext='.pkl')
            if not error:
                completed=True
    return error, completed, heading_toc

def code_extract(request, read, process_index, progress_index):
    error = False
    completed = False
    extract = Extract(request, read.doc)
    status = extract.check_toc()
    headings = []
    if status:
        headings = extract.heading_toc
        if(request.method=='POST'):
            start=request.POST['start']
            end=request.POST['end']
            error, start, end = validators.validate_page_range(request, start, end)
            if not error:
                if start is not None:
                    error, _ = extract.main(start,end)
                    if not error:
                        values=[extract.doc_text, extract.working_toc, extract.page_diff, extract.font_styles]
                        error, process = set.update_process(request, process_index, progress_index-1 ,1)
                        process =  get.process_all_db(request, process_index)
                        process.progress =  Process.progress_choices[progress_index][0]
                        if(not error):
                            error = actions.write(request, values, process)
                            if not error:
                                completed = True
                        else:
                            error = True
                            messages.warning(request, f'Your PDF file have no table of contents')
                        extract.doc.close()
    return error, completed, headings



