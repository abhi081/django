# myapp/urls.py

from django.urls import path
from .views import form_view, summary_view, login_or_register_view

urlpatterns = [
    path('', login_or_register_view, name='login_or_register'),
    path('form/', form_view, name='form'),
    path('summary/', summary_view, name='summary'),
]
