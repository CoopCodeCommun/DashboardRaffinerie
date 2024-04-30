import time, requests, os

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from dashboard_app.qonto_api import QontoApi
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import F
from django.utils.html import format_html
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboard_app.data import data
from dashboard_user.models import CustomUser, ContactProvisional
from dashboard_app.models import PrevisionCost, Recette, Groupe
from dashboard_app.models import (Contact, AccountAccount, AccountJournal, AccountAnalyticGroup, AccountAnalyticAccount, \
    RealCostInternSpending, RealCost, RealCostExternService, PrestationsVentsRecettesInt, Grant, Cost,
    OrganizationalChart, Badge, DepensesBienveillance, Pole, Configuration, Transaction)
from dashboard_app.odoo_api import OdooApi
from dashboard_app.serializers import (AccountAnalyticGroupSerializer, RealcostSerializer,
        PrestationsVentsRecettesIntValidator, PrevisionCostSerializer, RealCostExternServiceSerializer,
        RealCostIntSpendSerializer, PrestationsVentsRecettesIntSerializer,OrganizationalChartSerializer,
        TransactionSerializer)
from dashboard_app.models import AccountAccount
from cryptography.fernet import Fernet
from rest_framework.viewsets import ViewSet

# We'll create a fonction that will return a dictionary in the form adapted to
# the generale tables
def create_dict_with_data(slug_name, colonnes,lignes, total,new_ligne,new_line_name="", url_viewset="",titre_colonne=""):

    return {
        "slug": slug_name,
        "titre": titre_colonne,
        "colonnes": colonnes,
        "lignes": lignes,
        "total": total,
        "ajouter_ligne" : new_ligne,
        'new_line_name': new_line_name,
        'url_viewset': url_viewset
    }


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
    return render(request, 'dashboard/example.html', context=context)


def julienjs_suivi_budgetaire(request):
    context = {}
    return render(request, 'pages_html/suivi_budgetaire.html', context=context)
    pass


def edit_tableau_generique(request, table, index):
    table = getattr(data, table)
    ligne = table['lignes'][index]
    if request.GET.get('edit'):
        return render(request, 'dashboard/tableau_generique_ligne_edit.html', context={'ligne':ligne, 'table':table, 'index':index})
    else:
        return render(request, 'dashboard/tableau_generique_ligne_read.html', context={'ligne':ligne, 'table':table, 'index':index})


# in this method we will factorize the method of filtering the data for PrevisionCost,
# serializing and thant creating the data dictionary taht will send to the template
def refactor_cost_prev(model,data_type,type,name_table,serializer, total):
    # passing datas through the serializer by selecting the type of Cost Prevision
    queryset = model.filter(type__type=type)
    cost_serializer = serializer(queryset, many=True)
    # creating the dictionary that will send thee datas through context
    data_type['lines'] = cost_serializer.data
    data_type['total'] = total
    data_type['name_table'] = name_table+type
    data_type['columns'] = [{'nom':''}, {'nom':'amount'},{'nom':'editer'},{'nom':'effacer'}]
    data_type['list_include'] = ['titled', 'amount']
    data_type['new_line_name'] = 'prevision'+type
    data_type['url1'] ='suivi_budg'
    data_type['url2'] = 'depenses_recettes'

# Refacotr the method that will create the real cost table caring
# and intern service
def refactor_cost_reel(model,data_type,type,name_table,serializer, total):
    # passing datas through the serializer by selecting the type of Cost Prevision
    queryset = model.filter(type__type=type)
    cost_serializer = serializer(queryset, many=True)
    # creating the dictionary that will send thee datas through context
    data_type['lines'] = cost_serializer.data
    data_type['total'] = total
    data_type['name_table'] = name_table+type
    data_type['columns'] = [{'nom': ''},
                                  {'nom': 'date'},
                                  {'nom': 'proposition'},
                                  {'nom': 'validé'},
                                  {'nom': 'facturé'},
                                  {'nom': 'payé'},
                                  {'nom': 'editer'},
                                  {'nom':'effacer'}]
    data_type['list_include'] = ['username','date','proposition','validated', 'invoiced','payed']
    data_type['new_line_name'] = 'real_cost'+type
    data_type['url1'] ='suivi_budg'
    # unifying the type is CAR and IN_S. the value of the url will be used to select the
    # serializer in the reterive method so CAR and IN_S have the same serializer
    if type in ['CAR','IN_S']:
        data_type['url2'] = 'depenses_recettes2'
    else:
        data_type['url2'] = 'depenses_recettes' + type


# in this method we will factorize the method of filtering the data for Recettes,
# serializing and thant creating the data dictionary taht will send to the template
def refactor_recette(model,p_or_r,data_type,type,name_table,serializer, total):
    # passing datas through the serializer by selecting the type of Cost Prevision
    queryset = model.filter(prev_ou_reel=p_or_r,recette__type=type)
    cost_serializer = serializer(queryset, many=True)
    # creating the dictionary that will send thee datas through context
    data_type['lines'] = cost_serializer.data
    data_type['total'] = total
    data_type['name_table'] = name_table+p_or_r+type
    data_type['columns'] = [{'nom':''}, {'nom':'amount'},{'nom':'editer'},{'nom':'effacer'}]
    data_type['list_include'] = ['groupe_name', 'amount']
    data_type['new_line_name'] = 'recette'+p_or_r+type
    data_type['url1'] ='suivi_budg'
    data_type['url2'] = 'depenses_recettes5'



# Refacotr for retrive method in viewsets:
def refactor_retrive(model,given_pk, model_serializer):
    model_obj = model.objects.get(pk=given_pk)
    serialized_obj = model_serializer(model_obj, many=False)
    if serialized_obj.is_valid:
        return serialized_obj.data



# creating a refacor for destroyn selected object from all viewsets of Cost prevision
def destroy_refactor(given_pk, model):
    all_objects = model.objects.all()
    obj = get_object_or_404(all_objects, pk=given_pk)
    obj.delete()


# Creating a method that will send the total of amount or proposal of each table
def calculate_sub_total( model, calcul_object,recettes,prev_real=""):
    if recettes == False:

        # Calculate the sum of prices for each category of prevision cost real cost and Recette
        cost = model.objects.values('type__type').annotate(subtotal=Sum(calcul_object))
        # Convert the queryset of prevision, real_cost, recette to a dictionary
        return {item['type__type']: item['subtotal'] for item in cost}

    # The case of recettes is different because we've to specify if it is real or prevision cost
    # Here we do the first select where we group all types of reccettes in the categories
    # real or prevision cost
    recette = model.objects.values('prev_ou_reel','recette__type').annotate(subtotal=Sum(calcul_object))
    # here we construct two dictionaries with the subtotals for prevision and real cost
    return {item['recette__type']: item['subtotal'] for item in recette if item['prev_ou_reel']==prev_real}

# creating a viewset class for Caring (bienveillance) prevision cost table
class PrevisionBudgetCaringViewset(viewsets.ModelViewSet): #PrevisionBudgetCaringViewset
    def list(self, request):
        data_cost = {'CAR':{}, 'IN_S':{},'EX_S':{},'SP_I':{}}
        data_cost2 = {'CAR':{}, 'IN_S':{},'EX_S':{},'SP_I':{}}
        data_recette =  {'PP':{},'PV':{},'PR_IN':{},
                         'RP':{},'RV':{},'RR_IN':{}}

        for key, value in data_cost.items():
            refactor_cost_prev(PrevisionCost.objects.all(),
                               value, key, 'prev_cost_tab',
                               PrevisionCostSerializer, True)

            # creating the dictionary for real cost caring and intern service
            if key == 'CAR' or key == 'IN_S':
                refactor_cost_reel(RealCost.objects.all(),
                                   data_cost2[key], key, 'real_cost_tab',
                                   RealcostSerializer, True)

            elif key == 'EX_S':
                refactor_cost_reel(RealCostExternService.objects.all(),
                                   data_cost2[key], key, 'real_cost_tab',
                                   RealCostExternServiceSerializer, True)

            elif key == 'SP_I':
                refactor_cost_reel(RealCostInternSpending.objects.all(),
                                   data_cost2[key], key, 'real_cost_tab',
                                   RealCostIntSpendSerializer, True)


        # Adapting the columns on purchase and spending with
        # the given ones
        del data_cost2['EX_S']['columns'][4]
        data_cost2['EX_S']['list_include'] = ['contact_name', 'titled', 'date', 'validated', 'payed']


        data_cost2['SP_I']['columns'] = [{'nom': ''},{'nom': 'date'}, {'nom': 'montant'}, {'nom': 'editer'}, {'nom': 'effacer'}]
        data_cost2['SP_I']['list_include'] = ['pole_name', 'date_cost', 'amount']

        # creating the tables for recettes cases:
        model = PrestationsVentsRecettesInt.objects.all()
        for pr in ['P','R']:
            for v in ['P','V','R_IN']:
                refactor_recette(model,pr,
                                 data_recette[pr+v],v,'recette_prev_tab',PrestationsVentsRecettesIntSerializer,True)

        # Call the method that create the subtotals of amount or prevision
        sub_tot_prev_cost = calculate_sub_total(PrevisionCost, 'amount', False)
        sub_tot_real_cost_a = calculate_sub_total(RealCost, 'proposition', False)
        # sub_tot_real_cost_b = calculate_sub_total(RealCostExternService, 'proposition', False)
        sub_tot_real_cost_c = calculate_sub_total(RealCostInternSpending, 'amount', False)['SP_I']
        # Recettes
        sub_tot_recettes_a = calculate_sub_total(PrestationsVentsRecettesInt,
                                'amount', True, 'P')
        sub_tot_recettes_b = calculate_sub_total(PrestationsVentsRecettesInt,
                                                 'amount',True, 'R')
        print("Subtotal Recettes Reeles:   ",sub_tot_recettes_b['R_IN'])

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = {'base_template': base_template,
                   'data_cost': data_cost,
                   'data_cost2': data_cost2,
                   'data_recette': data_recette,
                   'sub_tot_prev_cost': sub_tot_prev_cost,
                   'sub_tot_real_cost_a': sub_tot_real_cost_a,
                   # 'sub_tot_real_cost_b': sub_tot_real_cost_b.EX_S,
                   'sub_tot_real_cost_c': sub_tot_real_cost_c,
                   'sub_tot_recettes_a': sub_tot_recettes_a,
                   'sub_tot_recettes_b': sub_tot_recettes_b,
                   }

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html',
                      context=context)


    def retrieve(self, request, pk=None):
        # prev_cost = PrevisionCost.objects.get(pk=pk)
        # prev_cost_serializer = PrevisionCostSerializer(prev_cost, many=False)
        prev_cost_ser_data = refactor_retrive(PrevisionCost,pk, PrevisionCostSerializer)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"


        if 'cancel' in request.GET:

            line = prev_cost_ser_data
            url1 ='suivi_budg'
            url2 = 'depenses_recettes'
            # Return the original table row HTML
            context = {
                'base_template': base_template, 'line': line,
                'url1': url1, 'url2': url2,
                'list': ['titled', 'amount']}

            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'edit_line/cost_prev_row_edit.html',
                      {'prev_cost_ser_data': prev_cost_ser_data})

    def create(self, request):
        serializer = PrevisionCostSerializer(data=request.data)
        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if serializer.is_valid():
            serializer.save()
            line = serializer.data
            url1 ='suivi_budg'
            url2 = 'depenses_recettes'


            context = {'base_template': base_template, 'line': line,
                       'url1': url1, 'url2': url2,
                       'list': ['titled', 'amount']}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
                'dashboard/tableau_generique_ligne_read.html',context=context)


    def update(self, request, pk=None):

        queryset = PrevisionCost.objects.all()
        car = get_object_or_404(queryset, pk=pk)
        serializer = PrevisionCostSerializer(car, data=request.data, partial=True)
        base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"

        if serializer.is_valid():
            serializer.save()
            line = serializer.data
            url1 ='suivi_budg'
            url2 = 'depenses_recettes'


            context = { 'base_template': base_template, 'line': line,
                        'url1': url1, 'url2': url2,
                       'list':['titled','amount']}
        else:
            context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk=None):
        # calling the refactor destroy to delete selected obj
        destroy_refactor(pk, PrevisionCost)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# create viewset class for Real cost of caring and intern service
class RealCostCaringInternServiceViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk=None):
        real_cost_serialized_data = refactor_retrive(RealCost,pk, RealcostSerializer)

        list = ['username','date','proposition','validated', 'invoiced','payed']

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if 'cancel' in request.GET:
            line = real_cost_serialized_data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettes2'
            # Return the original table row HTML
            context = {
                'base_template': base_template, 'line': line,
                'url1': url1, 'url2':url2,
                'list': list,
            }


            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'edit_line/cost_real_row_edit.html',
                      {'real_cost_serialized_data': real_cost_serialized_data})


    def create(self, request):
        # Verify why we can't pass imediatly request.data in Serializer...
        # answer: It seams that we interniens in the serializr by adding default data
        # like 'validated' = False we have to pass by a copy of request.POST -by modifying
        # the serializer we have to divert the non mutable condition.
        given_data = request.POST.copy()
        real_cost_serializer = RealcostSerializer(data=given_data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        # import ipdb; ipdb.set_trace()
        if real_cost_serializer.is_valid():
            real_cost_serializer.save()
            line = real_cost_serializer.data
            list = ['username','date','proposition','validated', 'invoiced','payed']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
                'dashboard/tableau_generique_ligne_read.html',context=context)



    def update(self, request, pk=None):
        queryset = RealCost.objects.all()
        cost_reel = get_object_or_404(queryset, pk=pk)
        given_data = request.POST.copy()
        serializer = RealcostSerializer(cost_reel, data=given_data, partial=True)

        list = ['username','date','proposition','validated', 'invoiced','payed']
        base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"

        if serializer.is_valid():
            serializer.save()
            line = serializer.data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettes2'
            context = { 'base_template': base_template, 'line': line,
                        'url1': url1, 'url2':url2,
                        'list':list}
        else:
            context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)



    def destroy(self, request, pk=None):
        # calling the refactor destroy to delete selected obj
        destroy_refactor(pk, RealCost)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# create viewset class for Real cost of caring and intern service
class RealCostPurchaseViewSet(viewsets.ModelViewSet):


    def retrieve(self, request, pk=None):

        purchase_serialized_data = refactor_retrive(RealCostExternService,pk, RealCostExternServiceSerializer)
        list = ['contact_name', 'titled', 'date', 'validated', 'payed']
        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if 'cancel' in request.GET:
            line = purchase_serialized_data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettesEX_S'
            # Return the original table row HTML
            context = {
                'base_template': base_template,
                'url1': url1, 'url2': url2,
                'line': line, 'list': list
            }

            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'edit_line/purchase_row_edit.html',
                      {'purchase_serialized_data': purchase_serialized_data})

    def create(self, request):
        given_data = request.POST.copy()
        purchase_serializer = RealCostExternServiceSerializer(data=given_data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if purchase_serializer.is_valid():
            purchase_serializer.save()
            line = purchase_serializer.data
            list = ['contact_name', 'titled', 'date', 'validated', 'invoiced', 'payed']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
                'dashboard/tableau_generique_ligne_read.html',context=context)


    def update(self, request, pk=None):
        queryset = RealCostExternService.objects.all()
        purchase_cost = get_object_or_404(queryset, pk=pk)
        given_data = request.POST.copy()
        serializer = RealCostExternServiceSerializer(purchase_cost, data=given_data, partial=True)

        list = ['contact_name', 'titled', 'date', 'validated', 'invoiced', 'payed']
        base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
        if serializer.is_valid():
            serializer.save()
            line = serializer.data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettesEX_S'
            context = { 'base_template': base_template, 'line': line,
                        'url1': url1, 'url2':url2,
                        'list':list}

        else:
            context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk=None):
        #calling the destroy refactor method to delete selected object
        destroy_refactor(pk, RealCostExternService)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# creating viewset class for intern real depenses
class RealInternSpendViewSet(viewsets.ModelViewSet):


    def retrieve(self, request, pk=None):
        intern_spending_data = refactor_retrive(RealCostInternSpending,pk, RealCostIntSpendSerializer)
        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        list = ['pole_name', 'date_cost', 'amount']

        if 'cancel' in request.GET:

            line = intern_spending_data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettesSP_I'
            # Return the original table row HTML
            context = {
                'base_template': base_template,
                'url1': url1, 'url2':url2,
                'line': line,'list': list
            }

            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'edit_line/intern_spend_row_edit.html',
                      {'intern_spending_data': intern_spending_data})

    def create(self,request):
        # given_data = request.POST.copy()
        intern_spending_serializer = RealCostIntSpendSerializer(data=request.data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if intern_spending_serializer.is_valid():
            intern_spending_serializer.save()
            line = intern_spending_serializer.data
            list = ['pole_name', 'date_cost', 'amount']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request, 'dashboard/tableau_generique_ligne_read.html',context=context)


    def update(self, request, pk=None):
        queryset = RealCostInternSpending.objects.all()
        intern_spending = get_object_or_404(queryset, pk=pk)
        serializer = RealCostIntSpendSerializer(intern_spending, data=request.data, partial=True)

        list = ['pole_name', 'date_cost', 'amount']
        base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
        if serializer.is_valid():
            serializer.save()
            line = serializer.data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettesSP_I'
            context = { 'base_template': base_template, 'line': line,
                        'url1': url1, 'url2': url2,
                        'list':list}

        else:
            context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk=None):
        #calling the destroy refactor method to delete selected object
        destroy_refactor(pk, RealCostInternSpending)

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)





# creating viewset class for recettes
class PrestationsVentsRecettesIntViewset(viewsets.ModelViewSet):


    def retrieve(self, request, pk=None):
        recette_serialized_data = refactor_retrive(PrestationsVentsRecettesInt,pk, PrestationsVentsRecettesIntSerializer)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        list = ['groupe_name', 'amount']

        # import ipdb; ipdb.set_trace()
        if 'cancel' in request.GET:

            line = recette_serialized_data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettes5'
            # Return the original table row HTML
            context = {
                'base_template': base_template,
                'url1': url1, 'url2': url2,
                'line': line, 'list': list
            }
            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                context=context)

        return render(request, 'edit_line/recette_row_edit.html',
        {'recette_serialized_data': recette_serialized_data})


    def create(self, request):
        recettes_serializer = PrestationsVentsRecettesIntSerializer(data=request.data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if recettes_serializer.is_valid():
            recettes_serializer.save()
            line = recettes_serializer.data
            list = ['groupe_name', 'amount']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
        'dashboard/tableau_generique_ligne_read.html',context=context)


    def update(self, request, pk=None):
        queryset = PrestationsVentsRecettesInt.objects.all()
        recette = get_object_or_404(queryset, pk=pk)
        serializer = PrestationsVentsRecettesIntSerializer(recette, data=request.data, partial=True)

        list = ['groupe_name', 'amount']
        base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"

        if serializer.is_valid():
            serializer.save()
            line = serializer.data
            url1 = 'suivi_budg'
            url2 = 'depenses_recettes5'

            context = { 'base_template': base_template, 'line': line,
                        'url1':url1, 'url2':url2, 'list':list}
        else:
            context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk):
        destroy_refactor(pk, PrestationsVentsRecettesInt)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# class viewset for organigramme
class OrganizationalChartViewSet(viewsets.ViewSet):
    # method for listing organigramme
    def list(self, request):
        organizational_chart_dt = {}
        queryset = OrganizationalChart.objects.all()

        organizational_chart_dt['lines'] = OrganizationalChartSerializer(queryset, many=True).data
        organizational_chart_dt['total'] = False
        organizational_chart_dt['name_table'] = 'organizational_tab'
        organizational_chart_dt['columns'] = [{'nom':''},
                                              {'nom':'presta interne'},
                                              {'nom':'garant du cadre'},
                                              {'nom':'référent budgt / subvention'},
                                              {'nom':'référent tâche planning'},
                                              {'nom':'editer'},
                                              {'nom':'effacer'}]

        organizational_chart_dt['list_include'] = ['username',
                                                   'intern_services',
                                                   'settlement_agent',
                                                   'budget_referee',
                                                   'task_planning_referee']

        organizational_chart_dt['new_line_name'] = 'organigramme_new'
        organizational_chart_dt['url1'] = 'suivi_budg'
        organizational_chart_dt['url2'] = 'organizationalchart'


        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = {
            'base_template': base_template,
            'organizational_chart_dt': organizational_chart_dt,
        }

        return render(request, 'dashboard/pages_html/organigramme.html', context=context)


    # method for creating organigramme
    def create(self, request):
        "Controleur pour POST"
        # Reciving data from new line and creating a new personne on organigramme
        given_data = request.POST.copy()
        org_chart_serializer = OrganizationalChartSerializer(data=given_data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if org_chart_serializer.is_valid():
            org_chart_serializer.save()
            line = org_chart_serializer.data
            list = ['username',
                    'intern_services',
                    'settlement_agent',
                    'budget_referee',
                    'task_planning_referee']


            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
        'dashboard/tableau_generique_ligne_read.html',context=context)


    def retrieve(self, request, pk=None):
        org_chart_serializet_dt = refactor_retrive(OrganizationalChart,pk, OrganizationalChartSerializer)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        list = ['username',
                'intern_services',
                'settlement_agent',
                'budget_referee',
                'task_planning_referee']

        # import ipdb; ipdb.set_trace()
        if 'cancel' in request.GET:

            line = org_chart_serializet_dt
            url1 = 'suivi_budg'
            url2 = 'organizationalchart'
            # Return the original table row HTML
            context = {
                'base_template': base_template,
                'url1':url1, 'url2':url2,
                'line': line, 'list': list
            }
            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                context=context)

        return render(request, 'edit_line/org_chart_row.html',
                      {'org_chart_serializet_dt': org_chart_serializet_dt})


    def update(self, request, pk=None):
        queryset = OrganizationalChart.objects.all()
        orga_chart = get_object_or_404(queryset, pk=pk)
        given_data = request.POST.copy()
        serializer = OrganizationalChartSerializer(orga_chart, data=given_data, partial=True)

        list = ['username',
                'intern_services',
                'settlement_agent',
                'budget_referee',
                'task_planning_referee']

        base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
        if serializer.is_valid():
            serializer.save()
            line = serializer.data
            # import ipdb; ipdb.set_trace()
            context = { 'base_template': base_template, 'line': line,
                        'list':list}
        else:
            context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)



    # Delete organizationalchart object
    def destroy(self, request, pk=None):
        destroy_refactor(pk, OrganizationalChart)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


def tableau_de_bord_perso(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'tableau_de_bord_perso.html', context=context)



def send_subventions(request):
    data1 = {}
    # Cherchons les données de la table subvention (Grant)
    subventions = Grant.objects.all()
    # Creat list of subventions for données de base
    subvention_donne_de_base_list = [[x.label, x.referee, x.partnaire, x.notification_date, x.reference] for x in subventions]
    # create the columns
    col_sub_base = [{'nom':''}, {'nom':'Référent'}, {'nom':'Partenaire'}, {'nom':'service'}, {'nom':'référence'}]
    # creating the dictionary with the data
    data1['subvention_donne_de_base'] = create_dict_with_data('donnees_de_base',col_sub_base,subvention_donne_de_base_list, True, False)

    # Subvention history part
    # Create history list
    subvention_historique_list = [[x.request_date, x.acceptation_date, x.notification_date, x.reference] for x in subventions]
    # column of history list
    col_history = [{'nom':''}, {'nom':'Demandée le'}, {'nom':'Acceptée le'}, {'nom':'Notifié le'}, {'nom':'référence'}]
    subvention_historique = create_dict_with_data('historique', col_history,subvention_historique_list,True, False)

    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,
        'data': data
    }
    return render(request, 'dashboard/pages_html/subventions.html', context=context)


'''
Sending data to the forms of nwe line in Prevision Cost tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''
# ------------ Start -------------------- #
# send data to Caring (bienveillance) form
def caring_data_form(request):
    cost_type = Cost.objects.get(type='CAR')
    tab_name = "prev_cost_tabCAR"
    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})


# send data to intern prevision cost form
def intern_serv_prev_form(request):
    cost_type = Cost.objects.get(type='IN_S')
    tab_name = "prev_cost_tabIN_S"

    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})


# send data to extern prevision cost form
def ext_serv_prev_form(request):
    cost_type = Cost.objects.get(type='EX_S')
    tab_name = "prev_cost_tabEX_S"

    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})

# send data to intern spendings cost form
def intern_spend_prev_form(request):
    cost_type = Cost.objects.get(type='SP_I')
    tab_name = "prev_cost_tabSP_I"

    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})


#---------------- FIN FORM NEW LINE PREV COST --------


'''
Sending data to the forms of nwe line in Real Cost tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''
# ------------ Start -------------------- #

# send data to Caring (bienveillance) real form
def real_caring_form(request):
    cost_type = Cost.objects.get(type='CAR')
    users = CustomUser.objects.all()
    us = users.last()
    tab_name = "real_cost_tabCAR"

    return render(request, 'new_lines/new_budget_cost_real.html',
                  {'cost_type': cost_type,
                        'tab_name': tab_name,
                        'users': users, 'us':us})


# send data to intern service real form
def real_in_s_form(request):
    cost_type = Cost.objects.get(type='IN_S')
    tab_name = "real_cost_tabIN_S"
    users = CustomUser.objects.all()

    return render(request, 'new_lines/new_budget_cost_real.html',
                  {'cost_type': cost_type,
                   'tab_name': tab_name,
                   'users': users})

# send data to real purchase form
def real_purchase_form(request):
    cost_type = Cost.objects.get(type='EX_S')
    tab_name = "real_cost_tabEX_S"
    # in the purchase case we send the contact and not the user
    contacts = ContactProvisional.objects.all()

    return render(request, 'new_lines/new_purchcase.html',
    {'cost_type': cost_type, 'tab_name': tab_name, 'contacts': contacts})


# send data to real intern spending form
def intern_spending_form(request):
    cost_type = Cost.objects.get(type='SP_I')
    tab_name = "real_cost_tabSP_I"
    # in the purchase case we send the contact and not the user
    poles = Pole.objects.all()

    return render(request, 'new_lines/new_intern_spend.html',
    {'cost_type': cost_type, 'tab_name': tab_name, 'poles': poles})


#---------------- FIN FORM NEW LINE PREV REAL COST --------

'''
Sending data to the forms of nwe line in Recettes real and prev tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''

# ------------ Start ----------------- #

# ___ Previstion
# form for Prestation prevision
def recette_prev_presta_form(request):
    recette = Recette.objects.get(type='P') # SUB   v   R_IN
    groupes = Groupe.objects.all()
    prev_ou_reel = 'P'
    tab_name = "recette_tabPP"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_prev_ventes_form(request):
    recette = Recette.objects.get(type='V')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'P'
    tab_name = "recette_tabPV"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
             'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_internes_form(request):
    recette = Recette.objects.get(type='R_IN')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'P'
    tab_name = "recette_tabPR_IN"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })


# ___ Real
# form for Prestation prevision
def recette_real_presta_form(request):
    recette = Recette.objects.get(type='P')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'R'
    tab_name = "recette_tabRP"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_real_ventes_form(request):
    recette = Recette.objects.get(type='V')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'R'
    tab_name = "recette_tabRV"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
             'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_internes_form_real(request):
    recette = Recette.objects.get(type='R_IN')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'R'
    tab_name = "recette_tabRR_IN"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })

#---------------- FIN FORM NEW LINE RECETTES --------


# send user to organigrame creating new line
def send_user_to_organigrame(request):
    users = CustomUser.objects.all()

    return render(request,
    'new_lines/new_organigramme.html',{'users': users})


################################

# methode generique qui va envoyer tous les données
def suivi_budgetaire(request):

    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,

    }
    return render(request, 'dashboard/pages_html/suivi_budgetaire.html', context=context)

#################################


def repertoire(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'repertoire.html', context=context)


def objectifs_indicateurs(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'objectifs_indicateurs.html', context=context)


### CONTROLEUR API ###

class AccountAnalyticGroupAPI(viewsets.ViewSet):
    # Un ViewSet est un outil qui permet te tout faire en un seul coup :
    # https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
    # On se sert d'un serializer pour formater la réponse et filtrer les données

    def list(self, request):
        # Pour récupérer tous les éléments
        serializer = AccountAnalyticGroupSerializer(AccountAnalyticGroup.objects.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Pour récupérer un seul élément avec le pk (primary key, ici, c'est un uuid4)
        serializer = AccountAnalyticGroupSerializer(AccountAnalyticGroup.objects.get(pk=pk))
        return Response(serializer.data)

    # Créer un élément. Il est parfois préférable de fabriquer un autre serializer qui va servir de formulaire de validation.
    # def create(self, request):
    #     serializer = CreateCardSerializer(data=json.loads(request.data.get('cards')), context={'request': request}, many=True)
    #     if serializer.is_valid():
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        # On peut choisir les permissions suivant l'action.
        # Par exemple pour créer ou détruire un objet, il faut être authentifié
        # if self.action in ['create', 'destroy']:
        #     permission_classes = [IsAuthenticated]
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class OdooContactsAPI(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # Récupération du contact demandé
        contact = Contact.objects.get(pk=pk)

        # Le retrieve est activé avec un hx-get :
        #     bouton cancel du tableau contact en mode écriture
        #     bouton modal du tableau contact
        #     bouton edit du tableau odoo contact

        if request.query_params.get('cancel'):
            return render(request, 'htmx/odoo_contacts_table_row.html', context={'contact': contact})

        if request.query_params.get('modal'):
            # Je simule un temps de chargement pour que tu puisse voir le spinner :)
            time.sleep(0.5)
            return render(request, 'htmx/odoo_contacts_modal_info.html', context={'contact': contact})

        # ce n'est ni un modal ni un cancel
        # Envoie du formulaire de modification du contact
        return render(request, 'htmx/odoo_contacts_edit_row.html', context={'contact': contact})

    def update(self, request, pk=None):
        # Le update est activé avec le hx-put du bouton save du tableau odoo contact
        contact = Contact.objects.get(pk=pk)

        # On récupère les données des formulaires et on remplace en base de donnée si nécessaire
        # Pas très élégant, on passera par un serializer pour faire ça proprement
        if request.data.get('nom') != contact.nom:
            contact.nom = request.data.get('nom')
        if request.data.get('structure') != contact.structure:
            contact.structure = request.data.get('structure')
        if request.data.get('adresse') != contact.adresse:
            contact.adresse = request.data.get('adresse')
        contact.save()

        return render(request, 'htmx/odoo_contacts_table_row.html', context={'contact': contact})

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


# Page d'exemple d'implémentation de l'API
def api_exemple(request):
    context = {}
    return render(request, 'api/from_api_exemple.html', context=context)


### PAGE D'EXAMPLE HTMX ###


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


# methode that will send the list of transactions from the datas
# that where saved on Transaction model
def qonto_transaction_all(request):
    #get the tansactions from the serializer
    queryset = Transaction.objects.order_by('-emitted_at')
    transactions = TransactionSerializer(queryset, many=True).data

    context ={'transactions': transactions}

    return render(request, 'api/qonto/qonto_transactions.html',
                  context=context)


# this method will send the particular transaction iformation to the modal
# or just the api iformation
def qonto_transaction_show(request, transaction_id):
    transaction, transaction_pk = None, ""
    obj_transac = Transaction.objects.get(pk=transaction_id)

    serialized_obj = TransactionSerializer(obj_transac, many=False)
    if serialized_obj.is_valid:
        transaction = serialized_obj.data
        transaction_pk = transaction.get('api_uuid')


    # Sending the url of the attachment
    attachment_hash = QontoApi().get_attachment(transaction_pk)
    message = attachment_hash['status']
    attach_yes = attachment_hash['attach_yes']
    attachments = None
    if attach_yes:
        attachments = attachment_hash['attachments']

    context = {'transaction': transaction, 'message': message,
               'attach_yes': attach_yes,'attachments': attachments}
    return render(request, 'api/qonto/transaction_modal.html',
                  context=context)

# Create a method that will update Qonto transactions data from the Qonto api
class qonto_transactions(View):

    @method_decorator(login_required)
    def get(self, request):
        qonto_api = QontoApi()
        qonto_api.get_all_transactions()
        messages.success(request, f"Transactions mises à jour. Total : {len(Transaction.objects.all())}")

        redirect('/admin/dashboard_app/transaction')



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
