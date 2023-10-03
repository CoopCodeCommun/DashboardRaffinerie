from django.urls import path
from .views import index, suivi_budgetaire, subventions, contacts, lazy_loading_profil_image, \
    reload_contact_from_odoo, odoo_account, organigramme, repertoire, objectifs_indicateurs, reload_account_from_odoo, \
    modal_contact
from django.conf import settings
from rest_framework import routers

urlpatterns = [
    # Pages d'exemple HTMX:
    path('contacts/', contacts, name="odoo_contacts"),
    path('odoo_account/', odoo_account, name="odoo_account"),
    path('lazy_loading_profil_image/<uuid:uuid>/', lazy_loading_profil_image.as_view(),
         name="lazy_loading_profil_image"),
    path('reload_contact_from_odoo/', reload_contact_from_odoo.as_view(), name="reload_contact_from_odoo"),
    path('reload_account_from_odoo/', reload_account_from_odoo.as_view(), name="reload_account_from_odoo"),
    path('modal_contact/<uuid:uuid>/', modal_contact.as_view(), name="modal_contact"),

    path('organigramme/', organigramme, name='organigramme'),
    path('suivi_budgetaire/', suivi_budgetaire, name='suivi_budgetaire'),
    path('subventions/', subventions, name='subventions'),
    path('repertoire/', repertoire, name='repertoire'),
    path('objectifs_indicateurs/', objectifs_indicateurs, name='objectifs_indicateurs'),
    path('', index, name='index'),
]
