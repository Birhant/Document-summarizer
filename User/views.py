from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .supporters import logics
from Processes.views import catch_error

#auth views
def check_session(func):
    def inner_function(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            messages.warning(request, "You are not authorized to access this page")
            return redirect('Home')
        else:
            return func(*args, **kwargs)
    return inner_function

signout=auth_views.LogoutView.as_view(template_name="User/signout.html")

class ChangePassword(auth_views.PasswordChangeView):
    from_class=PasswordChangeForm
    success_url = reverse_lazy('Home')

change_password=ChangePassword.as_view(template_name="User/change_password.html")

@check_session
@catch_error
def login_view(request):
    title = "Login"
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("Home")
    form = AuthenticationForm()
    return render(request,'User/login.html',{"title":title,"form":form})

def no_action(request):
    messages.warning(request, "Invalid URL pattern")
    return redirect('Home')

@catch_error
def signup(request):
    title="Signup"
    completed = False
    form, completed = logics.signup_logic(request)
    if completed:
        return redirect('Login')
    return render(request,'User/signup.html',{"title":title,"form":form})

@catch_error
def home(request):
    input, output, summarizers=logics.summarize_logic(request)
    title="Home"
    context={'title': title, 'summarizers': summarizers,'input': input, 'output': output}    
    return render(request,'index.html',context)

@login_required
@catch_error
def profile(request):
    title="Profile"
    context, completed=logics.update_profile_logic(request)
    if completed:
        return redirect('Profile')
    return render(request,"User/profile.html",{'title':title,'context':context})

