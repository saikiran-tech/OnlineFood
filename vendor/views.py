from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from foodapp.forms import UserProfileForm
from foodapp.models import UserProfile
from vendor.models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from foodapp.views import check_vendor_role
# Create your views here.

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