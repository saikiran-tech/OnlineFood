from django.shortcuts import render, redirect
from .models import User, UserProfile
from .forms import UserForm
from vendor.forms import VendorForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import detectUser, send_verification_email
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify
# Create your views here.
def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active =True)
    context = {
        'vendors': vendors
    }
    return render(request, 'home.html', context)


#Restrict vendor to access customer page
def check_vendor_role(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
    
#Restrict cust to access vendor page
def check_cust_role(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied
    


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
    elif request.method == "POST":
        form = UserForm(request.POST)
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
            #send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Account created successfully")
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registeredUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            
            vendor = v_form.save(commit=False)
            vendor.user = user  #assigned user to vendor
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile #assigned user_profile to vendor
            vendor.save()
            #send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Restaurent registered successfully")
            return redirect('registerVendor')
        else:
            print('Invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
                'form': form,
                'v_form': v_form
            }
    return render(request, 'accounts/registeredVendor.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, 'Congrats user is activated!')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
     
     


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
    elif request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, "Login successful!")
            return redirect('myAccount')
        else:
            messages.error(request, 'User is not approved.')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_cust_role)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')

def forgotPassword(request):
    if request.method=="POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            #send reset password email
            mail_subject = "Reset your password"
            email_template = 'accounts/emails/resetPasswordEmail.html'
            send_verification_email(request,user, mail_subject, email_template)
            messages.success(request, 'Password link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetPasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired!')
        return redirect('myAccount')


def resetPassword(request):
    if request.method=="POST":
        password = request.POST['password']
        confirm_passowrd = request.POST['confirm_password']

        if password == confirm_passowrd:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match')
            return redirect('resetPassword')
    return render(request, 'accounts/resetPassword.html')

