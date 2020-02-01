from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm,RegForm

def home(request):
    return render(request,"home.html",{'homepage':'欢迎来到网站'})

def login(request):
    '''username = request.POST.get('username','')
    password = request.POST.get('password','')
    refer = request.META.get('HTTP_REFERER', '/')
    user = auth.authenticate(request,username=username,password=password)
    if user:
        auth.login(request,user)
        return redirect(refer)
    else:
        return render(request,'home.html',{'homepage':'用户名或密码不正确'})'''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()

    context = {}

    context['loginform'] = login_form
    return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        register_form = RegForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username,email,password)
            user.save()
            #用户登录
            user = auth.authenticate(username = username,password = password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        register_form = RegForm()

    context = {}

    context['registerform'] = register_form
    return render(request,'register.html',context)
