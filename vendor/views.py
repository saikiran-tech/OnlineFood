from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from foodapp.forms import UserProfileForm
from foodapp.models import UserProfile
from vendor.models import Vendor
from menu.models import Category, Fooditem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from foodapp.views import check_vendor_role
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def v_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        v_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if p_form.is_valid() and v_form.is_valid():
            p_form.save()
            v_form.save()
            messages.success(request, 'Settings updated!')
            return redirect('v_profile')
        else:
            print(p_form.errors)
            print(v_form.errors)

    p_form = UserProfileForm(instance=profile)
    v_form = VendorForm(instance=vendor)

    context = {
        'p_form': p_form,
        'v_form': v_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'accounts/v_profile.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    
    context = {
        'categories': categories
    }
    return render(request, 'accounts/vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def fooditems_by_category(request, pk=None):
     
     vendor = get_vendor(request)
     category =  get_object_or_404(Category, pk=pk)
     fooditems = Fooditem.objects.filter(vendor=vendor, category=category)
     context = {
        'fooditems': fooditems,
        'category': category
     }


     return render(request, 'accounts/vendor/fooditems_by_category.html', context)


def add_category(request):
    if request.method=="POST":
        c_form = CategoryForm(request.POST)
        if c_form.is_valid():
            category_name = c_form.cleaned_data['category_name']
            category = c_form.save(commit=False)
            category.vendor = get_vendor(request)
           
            category.slug = slugify(category_name)
            c_form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('menu-builder')
    else:
        c_form = CategoryForm()
    context = {
        'c_form': c_form
    }
    return render(request, 'accounts/vendor/add_category.html', context)

def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method=="POST":
        c_form = CategoryForm(request.POST, instance=category)
        if c_form.is_valid():
            category_name = c_form.cleaned_data['category_name']
            category = c_form.save(commit=False)
            category.vendor = get_vendor(request)
           
            category.slug = slugify(category_name)
            c_form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('menu-builder')
    else:
        c_form = CategoryForm(instance=category)
        
    context = {
        'c_form': c_form,
        'category': category
    }
    return render(request, 'accounts/vendor/edit_category.html', context)


def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('menu-builder')