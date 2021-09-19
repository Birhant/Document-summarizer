from django import forms
from .models import Process


class UploadFileForm(forms. ModelForm):
    class Meta:
        model=Process
        fields={"file"}

class DecryptPDFForm(forms. Form):
    password= forms.CharField(max_length=32, widget=forms.PasswordInput)

class UploadMultipleFileForm(forms. Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={' multiple': True}))

class SearchFileForm(forms. Form):
    search = forms.CharField(max_length=240)
