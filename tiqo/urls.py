from django.urls import path
from .views import index
from django.conf import settings
from rest_framework import routers



urlpatterns = [
    path('', index, name='tiqo_index'),
]
