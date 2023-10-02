from django.urls import path
from .views import index, suivi_budgetaire, subventions, contacts, lazy_loading_profil_image, \
    reload_contact_from_odoo
from django.conf import settings
from rest_framework import routers

urlpatterns = [

    # Une api pour avoir la liste de tout les utilisateurs
    # ex :  curl http://localhost:8000/api/list_user/

    # Une api pour avoir l'information d'un utilisateur depuis son uuid
    # ex :  curl http://localhost:8000/api/user_solo/fb021856-973c-4d17-810d-d0cc4c8f3f84/
    path('suivi_budgetaire/', suivi_budgetaire, name='suivi_budgetaire'),
    path('subventions/', subventions, name='subventions'),  # Nouvelle URL pour la page "subventions"
    path('', index, name='index'),

    # Pages d'examples :
    path('contacts/', contacts, name="contacts"),

    # Rendu HTMX
    path('lazy_loading_profil_image/<uuid:uuid>/', lazy_loading_profil_image.as_view(), name="lazy_loading_profil_image"),
    path('reload_contact_from_odoo/', reload_contact_from_odoo.as_view(), name="reload_contact_from_odoo"),
]
