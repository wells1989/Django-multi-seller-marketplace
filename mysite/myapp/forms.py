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
        fields = ['username','email','first_name'] # standard fields for User model

    # NOTE: above, error if trying to put password and password1 in the fields array, hence separately defining them, will still show up on the form alongside the items in fields[] 

    """
    prior code (BUT, isn't called anywhere so not included in forms validation process)
    def check_password(self):
        if self.cleaned_data['password']!=self.cleaned_data['password2']:
            raise forms.ValidationError('Password fields do not match')
        return self.cleaned_data['password2']
    """
    
    # adding password match check to forms validation process
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        # above, using self.cleaned_data['field_name'] instead of self.field_name because the cleaned_data dictionary contains the validated (via the forms validation process) and cleaned values for all form fields

        if password and password2 and password != password2:
            raise forms.ValidationError('Password fields do not match')

        return cleaned_data
    