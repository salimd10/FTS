from django import forms
from FTS.models import *

class StaffRegForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = '__all__'
        print(fields)
        widgets = {
            'file_id': forms.TextInput(attrs={'class': "form-control", 'placeholder': "file_id"}),
        }

class LoginDetailsForm(forms.ModelForm):

    class Meta:
        model = StaffLogin
        fields = '__all__'

class AddFileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = '__all__'

class RmvLoginForm(forms.Form):
        user = forms.ModelMultipleChoiceField(queryset=Staff.objects.all())


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


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255)

    search.widget.attrs.update({'class': "form-control",
                                  'placeholder': "search",
                                  'name': "srch-term",
                                  'id': "srch-term"})











