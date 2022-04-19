from django.urls import path, include

from .views import home_view
# include this in main urls patterns
# path('', include("core.urls",namespace="core")),

app_name = 'core'

urlpatterns = [
    path('', home_view, name="home"),
]
