from django import forms
from .models import Product
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'file']


# from django.contrib.auth.models import User
class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','first_name'] 

    
    # adding password match check to forms validation process
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        # above, using self.cleaned_data['field_name'] instead of self.field_name because the cleaned_data dictionary contains the validated (via the forms validation process) and cleaned values for all form fields

        if password and password2 and password != password2:
            raise forms.ValidationError('Password fields do not match')

        return cleaned_data
    