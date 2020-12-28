from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('thank-you/', views.thank_you, name='thankyou'),
]