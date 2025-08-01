from django import forms
from .models import Category, Fooditem
from foodapp.validators import allowed_image_extensions

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allowed_image_extensions])
    class Meta:
        model = Fooditem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']