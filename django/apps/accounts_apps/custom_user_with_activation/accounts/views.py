from django.views.generic import DetailView,View
from django.views.generic.edit import FormMixin
from django.contrib.auth import views
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView)
from django.views import View
from django.views.generic import (CreateView, DetailView)
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse,reverse_lazy
from django.http import Http404
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe


from .forms import (LoginForm, RegistrationForm,EmailReactivation)
from .models import EmailActivation

User = get_user_model()


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('main:home') # does not work ??
 
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', None)
        login(self.request, form.get_user())
        if remember_me:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return super().dispatch(request, *args, **kwargs)
        raise Http404

    def get_redirect_url(self):
        redirect_to = self.success_url
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''


class UserLogoutView(LogoutView):
    next_page = 'accounts:login'


class UserProfileView(DetailView):
    queryset = User.objects.all()
    template_name = 'accounts/profile.html'
    slug_url_kwarg = 'user_slug'


class UserRegistrerView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/'


class EmailActivationView(FormMixin,View):
    success_url = reverse_lazy('accounts:login')
    form_class = EmailReactivation
    key = None

    def get(self,request,key=None,*args,**kwargs):
        self.key = key
        if key :
            forced_expired = None
            qs = EmailActivation.objects.filter(key__exact=key)
            url = reverse('accounts:login')
            if qs.count() == 1:
                confirm_qs = qs.confirmable()
                if confirm_qs.count() == 1:
                    obj = confirm_qs.first()
                    obj.activate()
                    
                    msg = '''
                        Your email has been confirmed successfully <br />
                        now you can Sign in. 
                        '''
                    messages.success(request,mark_safe(msg))
                    return redirect(url) 
                else:
                    activated_qs = qs.filter(activated=True)
                    if activated_qs.exists():
                        password_reset_url = reverse('accounts:password_reset')
                        msg = '''
                            Your email has been already confirmed <br />
                            do you need to 
                            <a href="{}">reset your password </a> ?
                        '''.format(password_reset_url)
                    else :
                        forced_expired_qs = qs.filter(forced_expired=True)
                        if forced_expired_qs.exists():
                            msg =  '''
                                     Your Account has been suspended
                                    '''
                    messages.success(request,mark_safe(msg))
                    return redirect(url)
        form = self.get_form()
        context = {'form':form,'key':key,'forced_expired':forced_expired}
        return render(request,'accounts/email_activation_error.html',context)

    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        msg = '''Email activation link has been sent please check your email.'''
        messages.success(self.request,msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation_email = EmailActivation.objects.create(user=user,email=email)
        new_activation_email.send_activation()
        return super().form_valid(form)



    def form_invalid(self,form):
        context = {'form':form,'key':self.key}
        return render(self.request,'accounts/email_activation_error.html',context)


