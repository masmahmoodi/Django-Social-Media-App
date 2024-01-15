from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisratoinForm,UserEditForm,ProfileEditForm
from .models import Profile
# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username=data.get('name'),password=data['password'])
            if user is not None:
                login(request,user)
                return HttpResponse('welcome')
            else:
                return HttpResponse('Invalid')
    else:
        form = LoginForm()
    return render(request,"users/login.html",{'form':form})


@login_required
def index(request):
    return render(request,"users/index.html")


def register(request):
    
    if request.method =="POST":
        form = UserRegisratoinForm(request.POST)
        if form.is_valid():
            if form.check_password():
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
                Profile.objects.create(user=new_user)
                return redirect('login')
            
    form = UserRegisratoinForm()
    return render(request,"users/register.html",{"form":form})


@login_required
def edit(request):
    if request.method =="POST":
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile
                                ,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)   
    return render(request,'users/edit.html',{"user_form":user_form,"profile_form":profile_form})                                  
                
