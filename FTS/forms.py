from django import forms
from FTS.models import *
from django_select2.forms import *

class admin_file_form(forms.Form):

    file = forms.ChoiceField(choices=[], widget=Select2Widget)

    def __init__(self, *args, **kwargs):
        mychoices = kwargs.pop('mychoices')
        mywidget = kwargs.pop('mywidget')
        super(admin_file_form, self).__init__(*args, *kwargs)
        self.fields['file'] = forms.ChoiceField(choices=mychoices, widget=mywidget)
        self.fields['file'].widget.attrs.update({'class': "form-control",
                                                     'style': "width:200px"

                                                     })




class admin_user_form(forms.Form):
    receiver = forms.ModelChoiceField(queryset=Staff.objects.exclude(admin_status=True), initial='',widget=Select2Widget)
    receiver.widget.attrs.update({'class': "form-control",
                                                 'style': "width:200px"

                                                 })

class staff_user_form(forms.Form):

    receiver = forms.ChoiceField(choices=[], widget=Select2Widget)

    def __init__(self, *args, **kwargs):
        mychoices = kwargs.pop('mychoices')
        mywidget = kwargs.pop('mywidget')
        super(staff_user_form, self).__init__(*args, *kwargs)
        self.fields['receiver'] = forms.ChoiceField(choices=mychoices, widget=mywidget)

        self.fields['receiver'].widget.attrs.update({'class': "form-control",
                                  'style': "width:200px"

                                  })

class StaffRegForm(forms.Form):
    staff_id = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20, empty_value='',required=False)
    admin_status = forms.BooleanField(initial=False,required=False)
    management_status = forms.BooleanField(initial=False, required=False)
    office = forms.ModelChoiceField(queryset=Office.objects.all(), initial='', widget=Select2Widget)

    staff_id.widget.attrs.update({'class': "form-control",
                                  'placeholder': "Staff Id",
                                  'id': "staff_id"

                                  })
    first_name.widget.attrs.update({'class': "form-control",
                                    'placeholder': "first name",
                                    'id': "first_name"
                                    })
    surname.widget.attrs.update({'class': "form-control",
                                 'placeholder': "surname",
                                 'id': "surname"
                                 })
    last_name.widget.attrs.update({'class': "form-control",
                                   'placeholder': "last name",
                                   'id': "last_name"
                                   })
    admin_status.widget.attrs.update({'class': "form-control",

                                     })
    management_status.widget.attrs.update({'class': "form-control",

                                      })

    office.widget.attrs.update({'class': "form-control",
                                'id': "office",
                                'placeholder': "Drop to select/search a department"})

    # class Meta:
    #     model = Staff
    #     fields = '__all__'
    #     print(fields)
    #     widgets = {
    #         'file_id': forms.TextInput(attrs={'class': "form-control", 'placeholder': "file_id"}),
    #    }


class LoginDetailsForm(forms.Form):
    username= forms.CharField(max_length=255)
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    staff = forms.ModelChoiceField(queryset=Staff.objects.all(), initial='',
                                      widget=Select2Widget)

    username.widget.attrs.update({'class': "form-control",
                                  'style':"width:400px"})
    password1.widget.attrs.update({'class': "form-control",
                                  'style': "width:400px"})
    password2.widget.attrs.update({'class': "form-control",
                                   'style': "width:400px"})

    staff.widget.attrs.update({'class': "form-control",
                               'style': "width:400px"})

class AddFileForm(forms.Form):
    file_id = forms.CharField(max_length=255)
    file_name = forms.CharField(max_length=400)

    file_id.widget.attrs.update({'class': "form-control",
                                  'style': "width:400px"})
    file_name.widget.attrs.update({'class': "form-control",
                                  'style': "width:400px"})


class RmvLoginForm(forms.Form):
        user = forms.ModelChoiceField(queryset=Staff.objects.all(), widget=Select2Widget)

        user.widget.attrs.update({'class': "form-control",
                                       'style': "width:400px"})


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
                                  'name': "q",
                                  'id': "srch-term"})

class LocateForm(forms.Form):
    locate = forms.CharField(max_length=255)

    locate.widget.attrs.update({'class': "form-control",
                                  'placeholder': "locate",
                                  'name': "q",
                                  'id': "srch-term"})











