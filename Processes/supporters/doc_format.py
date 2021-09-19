from Processes.supporters import actions
import re

def default(text):
    if text=='':
        text = "No text here"
    elif text==[]:
        text.append("No text here")
    return text


def prepare_format_0(doc_text):
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
    prepared_text = prepared_text[1:]
    return prepared_text

def summary_format_0(preprocessor, summarizer, prepared_text):
    summary = []
    for heading, text in prepared_text:
        if preprocessor is not None:
            text = preprocessor(text)
        summarized = summarizer( text )
        summary.append((heading,summarized))
    return summary


def summary_format_1(preprocessor, summarizer, prepared_text):
    summary = []
    for text in prepared_text:
        text = ''.join(text)
        if preprocessor is not None:
            text = preprocessor(text)
        summarized = summarizer( text ), 'para'
        summary.append(summarized)
    return summary

def export_format(doc_text):
    write_text = []
    try:
        new_doc_text = [(text[0], text[1].strip()) for text in doc_text]
        doc_text = new_doc_text
    except Exception:
        print('cleaning problem')
    for text in doc_text:
        try:
            if text==('','para'):
                continue
            heading = default(text[0][0]),text[0][1]
            para = (default(text[1]),'para')
        except Exception:
            heading = ('heading',"heading_1")
            para = ('text',"para")

        write_text.append(heading)
        write_text.append(para)
    #Check text
    default(write_text)
    return write_text

def get_text(content):
    tuples = tuple('a')
    if type(content) != type('string'):
        content = content[0]
    if type(content) == tuples:
        content = get_text(content)
    return content


def export_format_0(doc_text):
    write_text = []
    doc_text = [(text.strip(),'para') for text in doc_text]
    for text in doc_text:
        if text==('','para'):
            continue
        heading = ("keyword",'heading_1')
        para = (text,'para')
        write_text.append(heading)
        write_text.append(para)
    #Check text
    default(write_text)
    for i, text in enumerate(write_text.copy()):
        content = text[0]
        heading = text[1]
        content = get_text(content)
        write_text[i] = (content, heading)

    return write_text

