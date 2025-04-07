from django import forms
from .models import Vendor
from foodapp.validators import allowed_image_extensions
class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allowed_image_extensions])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
