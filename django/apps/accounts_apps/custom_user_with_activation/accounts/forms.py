from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

from .models import User,EmailActivation




class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email ", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=("Password "),
        strip=False,
        widget=forms.PasswordInput,
    )
    remember_me = forms.BooleanField(required=False,label='Remember me')

    def clean(self):
        email = self.cleaned_data.get('username')
        qs = User.objects.filter(email=email)
        if qs.exists():
            obj = qs.first()
            if obj.is_active == False:
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                path = reverse('accounts:email_resend_activate')
                if is_confirmable:
                    msg = '''we are already sent you an activation key to your email ,
                             please check your email. <br />
                             do you need to <a href="{}">resend activation key</a>
                          '''.format(path)
                    raise forms.ValidationError(mark_safe(msg))
                email_qs = EmailActivation.objects.email_exists(email)
                if email_qs.exists():
                    msg = '''
                            Please go <a href={}> here </a> to resend your activation email
                        '''.format(path)
                    raise forms.ValidationError(mark_safe(msg))
                raise forms.ValidationError('Your account is not activated yet')
        return super().clean()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username')

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]



class EmailReactivation(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if  not qs.exists():
            url = reverse('accounts:register')
            msg = '''
                    Email does not exists <br />
                    would you like to <a href='{}'>Sign up</a>
            '''.format(url)
            raise forms.ValidationError(mark_safe(msg))
        return email