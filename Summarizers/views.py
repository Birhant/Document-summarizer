from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from .models import PickledModel
from .forms import UploadForm
from .supporters.logics import upload_model_logic
from .supporters import get
from django.contrib import messages
from User.supporters import logics
from Processes.views import catch_error

def privilege(func):
    def inner_function(*args, **kwargs):
        request = args[0]
        if request.user.user_profile.acc_type == "Adm":
            return func(*args, **kwargs)
        else:
            messages.warning(request, "You are not authorized to access this page")
            return redirect('Home')
    return inner_function


@privilege
@login_required
@catch_error
def add_model(request):
    preprocessors=PickledModel.objects.filter(purpose="Preprocessor")
    preprocessor_choice=[("None",None)]
    for i in preprocessors.values():
        preprocessor_choice.append((i['name'],i['name']))
    if(request.method=="POST"):
        forms=UploadForm(request.POST,request.FILES)
        status = upload_model_logic(request, forms)
        if(status):
            return redirect("ShowModel")
    else:
        forms = UploadForm()
    title = "Add algorithms"
    context={"title": title, "form": forms, "preprocessor_choice": preprocessor_choice}
    return render(request, "PickledModel/add_model.html", context)

@privilege
@login_required
@catch_error
def show_model(request):
    title = "Show algorithms"
    models = get.all_models()
    return render(request, "PickledModel/show_model.html", {"title": title, "models": models})

