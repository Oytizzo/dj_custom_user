from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, get_user_model, logout

from .forms import UserCreationForm, UserLoginForm


def index(request):
    return HttpResponse("<h1>Hello world!</h1>")


def register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/login')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return HttpResponseRedirect("/")
    return render(request, 'accounts/login.html', {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")
