from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _
 
class RegistrationForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    mobileno = forms.CharField(widget=forms.TextInput(attrs=dict(max_length=16, validators=[phone_regex], blank=False, null=False,default='+91')), label=_("Contact Number"))
    firstname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("First Name"))
    lastname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Last Name"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    class Meta:
        model = User
        fields = ("username",)
        
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        self.instance.email = self.cleaned_data.get('email')
        self.instance.first_name = self.cleaned_data.get('firstname')
        self.instance.last_name = self.cleaned_data.get('lastname')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class TextForm(forms.ModelForm):


    text = forms.CharField(widget=forms.Textarea(attrs=dict(required=True, max_length=1000)), label=_("Text to append:"))
    filename = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)), label=_("filename"))    

    class Meta:
        model = User
        fields = ("text",)
