import os
import base64
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CustomRegisterForm, ImageForm
from .models import Image, USER

def home(request):
    return render(request, 'xxhungry/index.html')

def create_account(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        custom_form = CustomRegisterForm(request.POST)
        if form.is_valid() and custom_form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            custom_form.save()
            messages.success(request, f'Account created {username}!')
            return redirect('web-login')
        # else: # TODO: 1. check unfilled field and print out
        #     form = form.cleaned_data
        #     field_check = {"username", "email_address", "password", "reconfirm_password"}.difference(form.keys())
        #     print(field_check)
        #     messages.error(request, f'{list(field_check)[0]} is empty!')
    # else:
    #     form = RegisterForm()
    #     custom_form = CustomRegisterForm()
    return render(request, 'xxhungry/createaccount.html')

# def log_in(request):
#     users = User.objects.all()
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#
#         try:
#             user = users.get(username=username)
#             if password == user.password1:
#                 # login(request, user)
#                 return redirect('web-home')
#         except:
#             print("j")
#     return render(request, 'xxhungry/loginpage.html')

def log_out(request):
    if request.method == "POST":
        if "confirm" in request.POST:
            logout(request)
            return redirect('web-home')
    return render(request, 'xxhungry/logout1.html')

def upload_data(request):
    # print(request.method)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        # print(form.is_valid())
        if form.is_valid():
            image = Image(
                pest="",
                location="",
                author=request.user.id,
                host="",
                number=0,
                cum_num=0,
                image=request.FILES['image'])
            image.save()
            img_obj = image.image.url
            return render(request, 'xxhungry/uploaddata.html', {'form': form, 'img_obj': img_obj})
    return render(request, 'xxhungry/uploaddata.html')

def common_disease(request):
    return render(request, 'xxhungry/commondisease.html')

@login_required
def profile(request): # TODO: add back button, dynamic table
    images = Image.objects.all()
    path = ""
    obj = False
    if request.method == "POST":
        if "open" in request.POST:
            id = int(request.POST['open'])
            img = images.get(id=id).image_data
            base64_data = base64.b64encode(img).decode('utf-8')
            # path = str(images.get(id=id).image).replace('/', '\\')
            # path = os.path.join(r"\media", path)
            return render(request, 'xxhungry/usertable.html', {'images': images, 'img': base64_data})
        elif "edit" in request.POST:
            id = int(request.POST['edit'])
            obj = images.get(id=id)
            return render(request, 'xxhungry/usertable.html', {'images': images, 'img': path, 'obj': obj})
        elif "pest" in request.POST:
            id = request.POST['id']
            img = images.get(id=id)
            img.pest = request.POST['pest']
            img.location = request.POST['location']
            img.host = request.POST['host']
            img.number = request.POST['number']
            img.cum_num = request.POST['cum_num']
            img.save()
        elif "delete" in request.POST:
            id = request.POST['delete']
            img = images.get(id=id)
            img.delete()

        elif "search" in request.POST:
            search = request.POST['search']
            if search:
                result = Image.objects.filter(pest__contains=search).values() | Image.objects.filter(location__contains=search).values() | Image.objects.filter(host__contains=search).values()
                return render(request, 'xxhungry/usertable.html', {'images': result, 'img': path, 'obj': obj})


    return render(request, 'xxhungry/usertable.html', {'images': images, 'img': path, 'obj': obj})