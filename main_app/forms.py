from django.forms import ModelForm
from .models import *
from jsignature.widgets import JSignatureWidget
from jsignature.forms import JSignatureField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm

class MyCustomSignupForm(UserCreationForm):
    #email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(max_length=14)
    phone_no = forms.CharField(max_length=14)
    company_name = forms.CharField(max_length=14)
    department = forms.CharField(max_length=14)

    class Meta:
        model = User
        fields = ('position', 'first_name', 'last_name')


# class joinForm(ModelForm):
#     class Meta:
#         model = Join
#         fields = '__all__'
#
#
# class detailTransferForm(ModelForm):
#     class Meta:
#         model = Business
#         fields = ['company_name', 'company_number', 'industry', 'business_email', 'business_address']
#
# class businessForm(ModelForm):
#     invoice_footer = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 50}))
#     notes = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 50}))
#     class Meta:
#         model = Business
#         fields = '__all__'
#         exclude = ['filename_type1', 'filename_type2', 'slug']