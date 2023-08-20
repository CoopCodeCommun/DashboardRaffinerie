from django.urls import path
from .views import index, user_api, user_solo_api, suivi_budgetaire
from django.conf import settings
from rest_framework import routers





urlpatterns = [
    # ex :  curl http://localhost:8000/api/list_user/
    path('api/list_user/', user_api.as_view(), name='list_user'),

    # ex :  curl http://localhost:8000/api/user_solo/fb021856-973c-4d17-810d-d0cc4c8f3f84/
    path('api/user_solo/<uuid:uuid>/', user_solo_api.as_view(), name='user_solo_api'),

    path('suivi_budgetaire/', suivi_budgetaire, name='suivi_budgetaire'),
    path('', index, name='index'),
]
