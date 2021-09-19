from ..code.Summarizers import frequency_based_summarizer
from ..code.Summarizers import page_rank_summarizer
from ..code.Summarizers import tfidf_summarizer
from ..code.Summarizers import LexRank
from ..code.Summarizers import luhn_summarizer
from ..code.Summarizers import lsa_summarizer
from ..code.Summarizers import text_rank_summarizer
from ..code.Summarizers import frequency_matrix
#
from ..code.Preprocessors import strip
from ..code.Preprocessors import sumy_preprocess
from ..code.Preprocessors import freq
from ..code.Preprocessors import preprocess_tfidf
from ..code.Preprocessors import preprocess_pagerank
from ..code.Preprocessors import preprocess_freq
#
from ..models import PickledModel
from django.conf import settings
from django.contrib import messages
import pickle

default_summarizers={
    'frequency_based_summarizer':frequency_based_summarizer,
    'page_rank_summarizer':page_rank_summarizer,
    'tfidf_summarizer':tfidf_summarizer,
    'LexRank' :LexRank,
    'luhn_summarizer':luhn_summarizer,
    'lsa_summarizer':lsa_summarizer,
    'text_rank_summarizer':text_rank_summarizer,
    'frequency_matrix':frequency_matrix,
    #"text_rank":text_rank,
    #'spacy_code' :spacy_code,
}

default_preprocessor={
    'strip':strip,
    'freq':freq,
    'sumy_preprocess':sumy_preprocess,
    'preprocess_pagerank':preprocess_pagerank,
    'preprocess_tfidf':preprocess_tfidf,
    'preprocess_freq' :preprocess_freq,
    #'embedded':embedded,
}

def all_models():
    models=PickledModel.objects.all()
    return models

def all_summarizers():
    summarizers = []
    values = PickledModel.summarizer.all().values()
    for value in values:
        summarizer = {}
        summarizer['name'] = value['name']
        summarizers.append(summarizer)
    return summarizers

def all_summarizers_name():
    summarizers=[]
    values=PickledModel.summarizer.all().values()
    for value in values:
        summarizers.append(value['name'])
    return summarizers

def preprocessor(request, preprocessor_name):
    preprocessor = None
    error=False
    if(preprocessor_name != "" and preprocessor_name is not None and preprocessor_name != "None"):
        try:
            model = PickledModel.objects.get(name=preprocessor_name, purpose=PickledModel.purpose_choice[0][0])
            if(model.default):
                preprocessor=default_preprocessor[model.name].preprocess
            else:
                with open(settings.MEDIA_ROOT+model.file,'rb') as reader:
                    preprocessor=pickle.load(reader)
        except Exception:
            error=True
            messages.warning(request, f'Error occured while accessing preprocessor')
    return error, preprocessor

def summarizer(request, summarizer_name):
    model = PickledModel.summarizer.get(name=summarizer_name)
    summarizer_func = None
    error, preprocessor_func = preprocessor(request, model.preprocessor)
    if not error:

        if(model.default):
            summarizer=default_summarizers[model.name]
            summarizer_func = summarizer.summarize
        else:
            with open(settings.MEDIA_ROOT+model.file,'rb') as reader:
                summarizer_func=pickle.load(reader)

            error=False
            messages.warning(request, f'Error occured while accessing summarizer')
    return error, preprocessor_func, summarizer_func



def preprocessor1(request, preprocessor_name, input):
    error=False
    try:
        model = PickledModel.objects.get(name=preprocessor_name, purpose=PickledModel.purpose_choice[0][0])
        if(model.default):
            preprocessor=default_preprocessor[model.name]
            processed = preprocessor.preprocess(input)
        else:
            with open(settings.MEDIA_ROOT+model.file,'rb') as reader:
                preprocessor=pickle.load(reader)
            processed=preprocessor(input)
    except Exception:
        processed=input
        error=True
        messages.warning(request, f'Error occured while cleaning input text')
    return error, processed

def summarizer1(request, summarizer_name , input):
    model = PickledModel.summarizer.get(name=summarizer_name)
    error, processed = preprocessor(request, model.preprocessor, input)
    if not error:
        try:
            if(model.default):
                summarizer=default_summarizers[model.name]
                output=summarizer.summarize(request, processed)
            else:
                with open(settings.MEDIA_ROOT+model.file,'rb') as reader:
                    summarizer=pickle.load(reader)
                output=summarizer(processed)
        except Exception:
            error=True
            output = processed
            messages.warning(request, f'Error occured while summarizing text')
    else:
        output=input
    return error, output
