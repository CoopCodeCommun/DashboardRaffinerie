import time

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.html import format_html
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard_app.models import Contact, AccountAccount, AccountJournal, AccountAnalyticGroup, AccountAnalyticAccount
from dashboard_app.odoo_api import OdooApi
from dashboard_app.serializers import UserSerializer


# from rest_framework import routers, serializers, viewsets
# from rest_framework import viewsets,

def index(request):
    """
    Livre un template HTML
    Ne passe pas par l'api Django-Rest-Framework mais par le moteur de template de Django
    Template base.html dans le dossier templates
    avec un contexte qui contient le nom de l'utilisateur
    """
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'example.html', context=context)


def suivi_budgetaire(request):
    """
    Livre un template HTML suivi_budgetaire.html
    Extension du template base.html
    """
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'suivi_budgetaire.html', context=context)


def subventions(request):
    """
    Livre un template HTML subventions.html
    Extension du template base.html
    """
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'subventions.html', context=context)


def organigramme(request):
    """
    Livre un template HTML organigramme.html
    Extension du template base.html
    """
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'organigramme.html', context=context)


def repertoire(request):
    """
    Livre un template HTML organigramme.html
    Extension du template base.html
    """
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'repertoire.html', context=context)


def objectifs_indicateurs(request):
    """
    Livre un template HTML organigramme.html
    Extension du template base.html
    """
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'objectifs_indicateurs.html', context=context)


### TEST API AVEC MODEL USER ###

### PAGE D'EXAMPLE ###

def odoo_account(request):
    context = {
        "AccountAccounts": AccountAccount.objects.all().order_by('code'),
        "AccountJournals": AccountJournal.objects.all().order_by('name'),
        "AccountAnalyticGroup": AccountAnalyticGroup.objects.all().order_by('name'),
        "AccountAnalyticAccount": AccountAnalyticAccount.objects.all().order_by('code'),
    }
    return render(request, 'htmx/odoo_account.html', context=context)


@permission_classes([AllowAny])
class reload_account_from_odoo(APIView):
    def get(self, request, uuid=None):
        odooApi = OdooApi()
        odooApi.get_account_account()
        odooApi.get_account_journal()
        odooApi.get_account_analytic()
        context = {
            "AccountAccounts": AccountAccount.objects.all().order_by('code'),
            "AccountJournals": AccountJournal.objects.all().order_by('name'),
            "AccountAnalyticGroup": AccountAnalyticGroup.objects.all().order_by('name'),
            "AccountAnalyticAccount": AccountAnalyticAccount.objects.all().order_by('code'),
        }
        return render(request, 'htmx/odoo_account_button_dropdown.html', context=context)


def contacts(request):
    # On va chercher tout les objets de la table Contact
    # de la base de donnée (models.puy)
    # Pour l'exemple, on ne prend que ceux qui sont "Membership"
    contacts = Contact.objects.all()

    context = {
        'contacts': contacts[:5]
    }
    return render(request, 'htmx/odoo_contacts.html', context=context)


@permission_classes([AllowAny])
class reload_contact_from_odoo(APIView):
    def get(self, request, uuid=None):
        # Mise à jour la base de donnée depuis Odoo
        # requete appellé par le bouton "Mise à jour depuis Odoo"

        # pour simuler le spinner :
        # time.sleep(1)

        # Mise à jour la base de donnée depuis Odoo
        odooApi = OdooApi()
        contacts = odooApi.get_all_contacts()

        # On va chercher tous les objects Contact
        # dans la base de donnée mise à jour
        context = {
            'contacts': contacts[:10],
        }
        return render(request, 'htmx/odoo_contacts_table.html', context=context)


# HTMX USE CASES

@permission_classes([AllowAny])
class lazy_loading_profil_image(APIView):
    def get(self, request, uuid=None):
        context = {
            'contact': Contact.objects.get(pk=uuid)
        }
        return render(request, 'htmx/lazy_loading.html', context=context)
