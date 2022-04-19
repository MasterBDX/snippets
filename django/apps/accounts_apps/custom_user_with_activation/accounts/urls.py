from django.urls import path,re_path
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy

from .views import (UserLoginView, UserRegistrerView,
                    UserLogoutView, UserProfileView,
                    EmailActivationView
                    )


app_name = 'accounts'
urlpatterns = [
    
    # Password Change 
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'),
        name='password_change'
        ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'),
        name='password_change_done'
        ),
    
# Password Reset Password 
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',           
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url=reverse_lazy('accounts:password_reset_done')
            
            ),
        name='password_reset',
        ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done',
        ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('accounts:password_reset_complete'),
            template_name='accounts/password_reset_confirm.html',),
            name='password_reset_confirm',
        ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
        ),
    
    path('email-resend-activation/', EmailActivationView.as_view(),
             name='email_resend_activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrerView.as_view(), name='register'),
    path('<slug:user_slug>/', UserProfileView.as_view(), name='profile'),
    
    re_path('email-activation/(?P<key>[0-9,a-zA-Z]+)/$', EmailActivationView.as_view(),
             name='email_activate'),
    
]
