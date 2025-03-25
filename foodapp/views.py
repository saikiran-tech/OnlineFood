from django.shortcuts import render, redirect
from .models import User
from . import forms
from django.contrib import messages
# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = forms.UserForm(request.POST)
        if form.is_valid():
            #create the user using form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            #create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('registerUser')
    else:
        form = forms.UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registeredUser.html', context)

def home(request):
    return render(request, 'home.html')