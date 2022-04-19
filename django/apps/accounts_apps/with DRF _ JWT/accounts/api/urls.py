from django.urls import path

from .views import SignUpAPIView


app_name = 'accounts_api'

urlpatterns = [
    path('signup/',SignUpAPIView.as_view(),name="signup")
]