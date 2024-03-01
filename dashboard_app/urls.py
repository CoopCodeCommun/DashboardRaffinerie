from django.conf import settings
from django.urls import path, include
from . import views
from .views import (contacts, lazy_loading_profil_image, \
    reload_contact_from_odoo, odoo_account, reload_account_from_odoo, \
    AccountAnalyticGroupAPI, OdooContactsAPI, julienjs_suivi_budgetaire, OrganizationalChartViewSet,
    edit_tableau_generique, SuiviBudgetaireViewSet, PrevisionBudgetViewset)
from .views import index, send_subventions, suivi_budgetaire, repertoire, objectifs_indicateurs, api_exemple, tableau_de_bord_perso
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'account_analytic_group', AccountAnalyticGroupAPI, basename='account_analytic_group_api')
router.register(r'odoo_contacts', OdooContactsAPI, basename='odoo_contacts_api')
# creating router register for Budget Viewset
router.register(r'table_budgetaire', SuiviBudgetaireViewSet, basename='table_budgetaire')
# sending url url with new organigramme
router.register(r'organizationalchart', OrganizationalChartViewSet, basename='organizationalchart')
# Trying automus way:
router.register(r'prevision', PrevisionBudgetViewset, basename='budget_prevision')
urlpatterns = [

    # sending url with Viewset class
    path('suivi_budg/', include(router.urls)),
    # Pages d'exemple HTMX:
    path('organigramme_new/', views.send_user_to_organigrame, name='organigramme_new'),

    # url for the new line costs
    path('previsionCAR/', views.caring_data_form, name='previsionCAR'),
    path('new_line_prev_cost/', views.intern_serv_prev_form, name='new_line_prev_cost'),
    path('ext_prev_cost/', views.ext_serv_prev_form, name='ext_prev_cost'),
    path('intern_spend_prev/', views.intern_spend_prev_form, name='intern_spend_prev'),

    # url for the new line Recettes
    path('new_recette_1_prev/', views.recette_form_prev_1, name='new_recette_1_prev'),

    path('contacts/', contacts, name="odoo_contacts"),
    path('odoo_account/', odoo_account, name="odoo_account"),

    path('lazy_loading_profil_image/<uuid:uuid>/', lazy_loading_profil_image.as_view(),
         name="lazy_loading_profil_image"),
    path('reload_contact_from_odoo/', reload_contact_from_odoo.as_view(), name="reload_contact_from_odoo"),
    path('reload_account_from_odoo/', reload_account_from_odoo.as_view(), name="reload_account_from_odoo"),

    # Pages de l'application Front de Julien :
    path('suivi_budgetaire/', suivi_budgetaire, name='suivi_budgetaire'),
    path('julienjs/suivi_budgetaire/', julienjs_suivi_budgetaire, name='julienjs'),

    # Pour afficher une ligne editable :
    path('edit_tableau_generique/<str:table>/<int:index>/', edit_tableau_generique, name='edit_tableau_generique'),

    # A bosser :)
    #path('organigramme/', organigramme, name='organigramme'),
    path('tableau_de_bord_perso/', tableau_de_bord_perso, name='tableau_de_bord_perso'),
    path('subventions/', send_subventions, name='subventions'),
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
