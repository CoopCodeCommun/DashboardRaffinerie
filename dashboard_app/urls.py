from django.urls import path
from .views import index, user_api, user_solo_api, suivi_budgetaire, subventions, contacts
from django.conf import settings
from rest_framework import routers

urlpatterns = [

    # Une api pour avoir la liste de tout les utilisateurs
    # ex :  curl http://localhost:8000/api/list_user/
    path('api/list_user/', user_api.as_view(), name='list_user'),

    # Une api pour avoir l'information d'un utilisateur depuis son uuid
    # ex :  curl http://localhost:8000/api/user_solo/fb021856-973c-4d17-810d-d0cc4c8f3f84/
    path('api/user_solo/<uuid:uuid>/', user_solo_api.as_view(), name='user_solo_api'),

    path('suivi_budgetaire/', suivi_budgetaire, name='suivi_budgetaire'),
    path('subventions/', subventions, name='subventions'),  # Nouvelle URL pour la page "subventions"
    path('', index, name='index'),

    # Pages d'examples :
    path('contacts', contacts, name="contacts")
]
