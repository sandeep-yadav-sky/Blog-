from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
# Create your views here.
from .forms import SignUpForm, LoginForm, postform
from django.contrib.auth import authenticate, login, logout
from .models import post
from django.contrib.auth.models import Group
from django.core.cache import cache


def home(request):
    posts = post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST, data=request.POST)
            if(form.is_valid()):
                uname = form.cleaned_data['username']
                passw = form.cleaned_data['password']
                user = authenticate(username=uname, password=passw)
                if(user is not None):
                    login(request, user)
                    messages.success(
                        request, 'congratulations You have successfully loged in')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def contact(request):
    if request.user.is_authenticated:
        return render(request, 'blog/contact.html')
    else:
        return HttpResponseRedirect('/login/')


def dashboard(request):
    if request.user.is_authenticated:
        posts = post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        ct = cache.get('count',version = user.pk)
        ip = request.session.get('ip',0)
        return render(request, 'blog/dashboard.html', {'ct': ct, 'ip':ip, 'posts': posts, 'full_name': full_name, 'groups': gps})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            messages.success(
                request, 'congratulations You have successfully loged in')
            user = form.save()
            group = Group.objects.get(name='author')
            user.groups.add(group)
            return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = postform(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                pst = post(title=title, desc=desc)
                pst.save()
        else:
            fm = postform()
        return render(request, 'blog/addpost.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


def Edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            eo = post.objects.get(pk=id)
            fm = postform(request.POST, instance=eo)
            if fm.is_valid():
                fm.save()
        else:
            eo = post.objects.get(pk=id)
            fm = postform(instance=eo)
        return render(request, 'blog/updatepost.html', {'form': fm, 'ob': eo})
    else:
        return HttpResponseRedirect('/login/')


def Delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            do = post.objects.get(pk=id)
            do.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
