from django import forms
from FTS.models import *

class StaffRegForm(forms.ModelForm):
    # first_name = forms.CharField()
    # surname = forms.CharField()
    # last_name = forms.CharField()
    # staff_id = forms.CharField()
    # password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    # password2 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    # admin_status = forms.ChoiceField(choices=(("True", "True"), ("False", "False")), required=True)

    class Meta:
        model = Staff
        fields = '__all__'

class LoginDetailsForm(forms.ModelForm):

    class Meta:
        model = StaffLogin
        fields = '__all__'

class AddFileForm(forms.Form):
    file_id = forms.CharField(max_length=30)
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=50)


class StaffLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    username.widget.attrs.update({'class': "form-control",
                                  'placeholder': "Username",
                                  'data-rule': "minlen:20",
                                  'data-msg': "Please enter at least 8 chars"})
    password.widget.attrs.update({'class': "form-control",
                                  'placeholder': "Password",
                                  'data-rule': "minlen:20",
                                  'data-msg': "Please enter at least 8 chars"})











