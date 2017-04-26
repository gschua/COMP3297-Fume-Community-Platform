from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

User = get_user_model()

class UserLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Incorrect login informatin")

        if not user.is_active:
            raise forms.ValidationError("This user is no longer active")
        #default
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Comfirm password')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been used")

        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password!=password2:
            raise forms.ValidationError("Password inconsistent")

        return password

class UserChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label='New email')
    new_email2 = forms.EmailField(label='Comfirm new email')

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')

        email_qs = User.objects.filter(email=new_email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been used")

        return new_email
    def clean_new_email2(self):
        new_email = self.cleaned_data.get('new_email')
        new_email2 = self.cleaned_data.get('new_email2')
        
        if new_email!=new_email2:
            raise forms.ValidationError("Email inconsistent")

        return new_email2
