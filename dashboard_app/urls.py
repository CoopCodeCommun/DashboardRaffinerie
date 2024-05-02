from django.conf import settings
from django.urls import path, include
from . import views
from dashboard_app.views import (contacts, lazy_loading_profil_image,qonto_transactions,
        qonto_transaction_all,\
        reload_contact_from_odoo, odoo_account, reload_account_from_odoo, AccountAnalyticGroupAPI,
        OdooContactsAPI, julienjs_suivi_budgetaire, OrganizationalChartViewSet, edit_tableau_generique,
        PrevisionBudgetCaringViewset, RealCostCaringInternServiceViewSet,
        RealCostPurchaseViewSet, RealInternSpendViewSet, PrestationsVentsRecettesIntViewset)
from dashboard_app.views import index, send_subventions, suivi_budgetaire, repertoire, objectifs_indicateurs, api_exemple, tableau_de_bord_perso
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'account_analytic_group', AccountAnalyticGroupAPI, basename='account_analytic_group_api')
router.register(r'odoo_contacts', OdooContactsAPI, basename='odoo_contacts_api')
# creating router register for Budget Viewset
# sending url url with new organigramme
router.register(r'organizationalchart', OrganizationalChartViewSet, basename='organizationalchart')
# Trying automus way:
router.register(r'depenses_recettes', PrevisionBudgetCaringViewset, basename='depenses_recettes')
router.register(r'depenses_recettes2', RealCostCaringInternServiceViewSet, basename='depenses_recettes2')
router.register(r'depenses_recettesEX_S', RealCostPurchaseViewSet, basename='depenses_recettesEX_S')
router.register(r'depenses_recettesSP_I', RealInternSpendViewSet, basename='depenses_recettesSP_I')
router.register(r'depenses_recettes5', PrestationsVentsRecettesIntViewset, basename='depenses_recettes5')

# Combining the viewset in purpose to have same url
# router.register(r'prevision2', CombinedView.as_view(), basename='prevision')

urlpatterns = [
    # sending url with Viewset class
    path('suivi_budg/', include(router.urls)),
    # Pages d'exemple HTMX:
    path('organigramme_new/', views.send_user_to_organigrame, name='organigramme_new'),

    # url for the new line costs for prevision and real
    # prevision
    path('previsionCAR/', views.caring_data_form, name='previsionCAR'),
    path('previsionIN_S/', views.intern_serv_prev_form, name='previsionIN_S'),
    path('previsionEX_S/', views.ext_serv_prev_form, name='previsionEX_S'),
    path('previsionSP_I/', views.intern_spend_prev_form, name='previsionSP_I'),
    # real
    path('real_costCAR/', views.real_caring_form, name='real_costCAR'),
    path('real_costIN_S/', views.real_in_s_form, name='real_costIN_S'),
    path('real_costEX_S/', views.real_purchase_form, name='real_costEX_S'),
    path('real_costSP_I/', views.intern_spending_form, name='real_costSP_I'),

    # url for the new line Recettes Prevision et Reel
    # Prevision
    path('recettePP/', views.recette_prev_presta_form, name='recette_tabPP'),
    path('recettePV/', views.recette_prev_ventes_form, name='recette_tabPV'),
    path('recettePR_IN/', views.recette_internes_form, name='recette_tabPR_IN'),
    # Real
    path('recetteRP/', views.recette_real_presta_form, name='recette_tabRP'),
    path('recetteRV/', views.recette_real_ventes_form, name='recette_tabRV'),
    path('recetteRR_IN/', views.recette_internes_form_real, name='recette_tabRR_IN'),

    path('contacts/', contacts, name="odoo_contacts"),
    # refreshing qonto transactions
    path('qonto_transactions/', qonto_transaction_all, name="qonto_transactions_all"),
    path('qonto_transactions/<uuid:transaction_id>/', views.qonto_transaction_show, name="qonto_transactions_show" ),

    path('action/qonto_transactions/', qonto_transactions.as_view(), name="qonto_transactions"),
    path('odoo_account/', odoo_account, name="odoo_account"),

    path('lazy_loading_profil_image/<uuid:uuid>/', lazy_loading_profil_image.as_view(),
         name="lazy_loading_profil_image"),
    path('reload_contact_from_odoo/', reload_contact_from_odoo.as_view(), name="reload_contact_from_odoo"),
    path('reload_account_from_odoo/', reload_account_from_odoo.as_view(), name="reload_account_from_odoo"),

    # Pages de l'application Front de Julien :
    path('julienjs/suivi_budgetaire/', julienjs_suivi_budgetaire, name='julienjs'),

    # Pour afficher une ligne editable :
    path('edit_tableau_generique/<str:table>/<int:index>/', edit_tableau_generique, name='edit_tableau_generique'),

    # A bosser :)
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
    path('test_columns', views.test_columns, name='test_columns')
]
