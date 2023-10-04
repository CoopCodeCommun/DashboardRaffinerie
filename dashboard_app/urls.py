from django.conf import settings
from django.urls import path, include
from .views import contacts, lazy_loading_profil_image, \
    reload_contact_from_odoo, odoo_account, reload_account_from_odoo, \
    AccountAnalyticGroupAPI, OdooContactsAPI
from .views import index, suivi_budgetaire, subventions, organigramme, repertoire, objectifs_indicateurs, api_exemple
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'account_analytic_group', AccountAnalyticGroupAPI, basename='account_analytic_group_api')
router.register(r'odoo_contacts', OdooContactsAPI, basename='odoo_contacts_api')

urlpatterns = [
    # Pages d'exemple HTMX:
    path('contacts/', contacts, name="odoo_contacts"),
    path('odoo_account/', odoo_account, name="odoo_account"),

    path('lazy_loading_profil_image/<uuid:uuid>/', lazy_loading_profil_image.as_view(),
         name="lazy_loading_profil_image"),
    path('reload_contact_from_odoo/', reload_contact_from_odoo.as_view(), name="reload_contact_from_odoo"),
    path('reload_account_from_odoo/', reload_account_from_odoo.as_view(), name="reload_account_from_odoo"),

    # Pages de l'application Front de Julien :
    path('organigramme/', organigramme, name='organigramme'),
    path('suivi_budgetaire/', suivi_budgetaire, name='suivi_budgetaire'),
    path('subventions/', subventions, name='subventions'),
    path('repertoire/', repertoire, name='repertoire'),
    path('objectifs_indicateurs/', objectifs_indicateurs, name='objectifs_indicateurs'),

    # API Django-Rest-Framework
    # Les routes ViewSet sont déclarés un peu différemment,
    # avec un router qui dirige les GET/POST/PUT/DELETE, juste avant les routes de l'application.
    path('api/', include(router.urls)),
    # La page d'exemple d'implémentation de l'API
    path('api_exemple/', api_exemple, name='api_exemple'),

    path('', index, name='index'),
]
