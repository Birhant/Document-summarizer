from Summarizers.supporters.get import preprocessor
from django import forms
from django.forms import widgets
from .models import PickledModel
from django.core.exceptions import ValidationError
import os

def validate(value):
    path=value.url
    valid_types=[".pk"]
    _,base=os.path.split(path)
    name,ext=os.path.splitext(base)
    if(ext in valid_types):
        return value
    else:
        return ValidationError("The file must be "+str(valid_types))

class UploadModelForm(forms.ModelForm):
    class Meta:
        model=PickledModel
        fields={"file"}

class UploadFileForm(forms.ModelForm):
    class Meta:
        model=PickledModel
        fields={"file"}

class UploadForm(forms.Form):
    file=forms.FileField(allow_empty_file=True, required=False, initial=None)
    name = forms.CharField(max_length = 100)
    purpose = forms.ChoiceField(choices=list(PickledModel.purpose_choice))
    default=forms.BooleanField(initial=False, required=False)
    accuracy = forms.ChoiceField(choices=list(PickledModel.accuracy_choice))

