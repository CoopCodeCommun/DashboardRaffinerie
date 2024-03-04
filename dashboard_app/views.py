import time

from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.utils.html import format_html
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboard_app.data import data
from dashboard_user.models import CustomUser
from dashboard_app.models import PrevisionCost, Recette
from dashboard_app.models import (Contact, AccountAccount, AccountJournal, AccountAnalyticGroup, AccountAnalyticAccount, \
    RealCostInternSpending, RealCost, RealCostExternService, PrestationsVentsRecettesInt, Grant, Cost,
    OrganizationalChart, Badge, DepensesBienveillance)
from dashboard_app.odoo_api import OdooApi
from dashboard_app.serializers import UserSerializer
from dashboard_app.serializers import (AccountAnalyticGroupSerializer, OrganizationalChartValidator, RealcostSerializer,
                          PrestationsVentsRecettesIntValidator, PrevisionCostSerializer)
from dashboard_app.models import AccountAccount
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


#Add edit and efface  buton lines
def edit_efface(list): # A ajoutter dans la classe SuviBudgetaireViewSet
    pass
    # for l in list:
    #     l['edit'] = l['pk']
    #     l['efface'] = l['pk']

# creating a method that returns the columns for the prevision cost
def columns_buget_prev():
    return [{'nom':''}, {'nom':'amount'},{'nom':'edit'},{'nom':'efface'}]


# in this method we will factorize the method of filtering the data for PrevisionCost,
# serializing and thant creating the data dictionary taht will send to the template
def refactor_cost_prev(data_type,type):
    # passing datas through the serializer by selecting the type of Cost Prevision
    queryset = PrevisionCost.objects.filter(type__type=type)
    prev_cost_serializer = PrevisionCostSerializer(queryset, many=True)
    # creating the dictionary that will send thee datas through context
    data_type['lines'] = prev_cost_serializer.data
    data_type['name_table'] = 'prev_cost_tab'
    data_type['columns'] = columns_buget_prev()
    data_type['list_include'] = ['titled', 'amount']
    data_type['new_line_name'] = 'prevision'+type


# creating a refacor for creating method for all viewsets of Cost prevision
def create_refacor(given_data):
    serializer = PrevisionCostSerializer(data=given_data)
    if serializer.is_valid():
        serializer.save()

        return serializer.data


# creating a refacor for updating selected object from all viewsets of Cost prevision
def update_refacrot(given_pk, given_data):
    queryset = PrevisionCost.objects.all()
    get_query = get_object_or_404(queryset, pk=given_pk)
    serializer = PrevisionCostSerializer(get_query, data=given_data, partial=True)

    if serializer.is_valid():
        serializer.save()

        return serializer.data


# creating a refacor for destroyn selected object from all viewsets of Cost prevision
def destroy_refacrot(given_pk):
    all_objects = PrevisionCost.objects.all()
    obj = get_object_or_404(all_objects, pk=given_pk)
    obj.delete()


# creating a viewset class for Caring (bienveillance) prevision cost table
class PrevisionBudgetCaringViewset(viewsets.ModelViewSet): #PrevisionBudgetCaringViewset
    def list(self, request):
        prevision_cost = {}

        refactor_cost_prev(prevision_cost, 'CAR')
        # taking datas from the serializer
        # queryset = PrevisionCost.objects.filter(type__type='CAR')
        # prev_cost_serializer = PrevisionCostSerializer(queryset, many=True)
        # # creating the dictionary that will send thee datas through context
        # prevision_cost['lines'] = prev_cost_serializer.data
        # prevision_cost['name_table'] = 'prev_cost_tab'
        # prevision_cost['columns'] = columns_buget_prev()
        # prevision_cost['list_include'] = ['titled','amount']
        # prevision_cost['new_line_name'] = 'previsionCAR'

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = { 'base_template': base_template,'prevision_cost': prevision_cost}

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html', context=context)


    def retrieve(self, request, pk=None):
        prev_cost = PrevisionCost.objects.get(pk=pk)
        prev_cost_serializer = PrevisionCostSerializer(prev_cost, many=False)

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"

        if 'cancel' in request.GET:

            line = prev_cost_serializer.data
            # Return the original table row HTML
            context = {'base_template': base_template, 'line': line, 'list': ['titled', 'amount']}

            return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)

        return render(request, 'htmx/cost_prev_row_edit.html', {'prev_cost_serializer': prev_cost_serializer})

    def create(self, request):
        line = create_refacor(request.data)
        # import ipdb; ipdb.set_trace()

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = {'base_template': base_template, 'line': line, 'list': ['titled', 'amount']}

        return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)


    def update(self, request, pk=None):
        line = update_refacrot(pk,request.data)

        # queryset = PrevisionCost.objects.all()
        # car = get_object_or_404(queryset, pk=pk)
        # serializer = PrevisionCostSerializer(car, data=request.data, partial=True)
        #
        # if serializer.is_valid():
        #     serializer.save()
        #
        #     line = serializer.data

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = { 'base_template': base_template, 'line': line, 'list':['titled','amount']}

        return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)


    def destroy(self, request, pk=None):
        destroy_refacrot(pk)

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)


# creating a viewset class for Intern Service prevision cost table
class PrevisionCostInterService(viewsets.ModelViewSet):
    def list(self, request):
        prevision_intern_service = {}
        # calling the refactor method who does the queryset and the
        refactor_cost_prev(prevision_intern_service,'IN_S')

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = { 'base_template': base_template,'prevision_intern_service': prevision_intern_service}

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html', context=context)



    def retrieve(self, request, pk=None):
        prev_cost = PrevisionCost.objects.get(pk=pk)
        prev_cost_serializer = PrevisionCostSerializer(prev_cost, many=False)

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"

        if 'cancel' in request.GET:

            line = prev_cost_serializer.data
            # Return the original table row HTML
            context = {'base_template': base_template, 'line': line, 'list': ['titled', 'amount']}

            return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)

        return render(request, 'htmx/cost_prev_row_edit.html', {'prev_cost_serializer': prev_cost_serializer})


    def create(self, request):
        line = create_refacor(request.data)
        # import ipdb; ipdb.set_trace()

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = {'base_template': base_template, 'line': line, 'list': ['titled', 'amount']}

        return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)


    def update(self,request,pk=None):
        line = update_refacrot(pk,request.data)

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = { 'base_template': base_template, 'line': line, 'list':['titled','amount']}

        return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)



    def destroy(self,request,pk=None):
        line = destroy_refacrot(pk)

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = { 'base_template': base_template, 'line': line, 'list':['titled','amount']}

        return render(request, 'dashboard/tableau_generique_ligne_read.html', context=context)


'''
# gathering viewset so we can have the same url
class PrevisionBudgetRouter(APIView):
    def get(self, request, *args, **kwargs):
        type_param = request.query_params.get('type', None)
        if type_param == 'CAR':
            viewset = PrevisionBudgetCaringViewset.as_view({'get': 'list'})
        elif type_param == 'IN_S':
            viewset = PrevisionCostInterService.as_view({'get': 'list'})
        else:
            return Response({"error": "Invalid type parameter"}, status=status.HTTP_400_BAD_REQUEST)

        return viewset(request, *args, **kwargs)
'''


# suivi budgetaire with Vieset
class SuiviBudgetaireViewSet(viewsets.ViewSet):
    def list(self, request):
        "Controleur pour GET"

        '''
            TESTING OTHER KIND OF TEMPLATE
        '''
        # the data0 dictionary will serve gatherign data of different cases
        data0 = {}
        data1 = {}

        # base de colonnes pour les suivies budgetaires prévisions
        col_prevision = [
                # A verifier s'il faut 'list': True  OU 'input': True ???
                {'nom':'','list': True},
                {'nom':'amount', 'input': True},
                {'nom':'', 'input': False},
                {'nom':'', 'input': False}
            ]

        # On va recupperer toute les données de prevision pour les filtrer par la suite
        prev_cost = PrevisionCost.objects.all()

        # filtrons pour  Caring (bienveillance)
        prev_cost_caring_filt = prev_cost.filter(type__type='CAR')
        prev_cost_caring_dict = prev_cost_caring_filt.values('pk', 'titled','amount')
        # add edit and efface button
        for l in prev_cost_caring_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']
        data1['prev_cost_caring'] = create_dict_with_data( "prev_beinveillance", col_prevision, prev_cost_caring_dict, True, True, new_line_name='new_prev_bienveillance',url_viewset='/suivi_budg/table_budgetaire/')

        # filtrons pour  Interne services (Prestation internes)
        prev_intern_service_cost_filt = prev_cost.filter(type__type='IN_S')
        prev_intern_service_cost_dict = prev_intern_service_cost_filt.values('pk', 'titled','amount')
        for l in prev_intern_service_cost_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']
        data1['prev_intern_service_cost'] = create_dict_with_data('prev_intern_serv',col_prevision, prev_intern_service_cost_dict, True, True, new_line_name='new_line_prev_cost', url_viewset='/suivi_budg/table_budgetaire/')

        # filtrons pour  Extern service (Prestation externes achats)
        prev_ext_service_cost_filt = prev_cost.filter(type__type='EX_S')
        prev_ext_service_cost_dict = prev_ext_service_cost_filt.values('pk', 'titled','amount')
        for l in prev_ext_service_cost_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']

        # creons la bd pour les prestations externes prevision
        data1['prev_ext_service_cost'] = create_dict_with_data('recap_recettes',col_prevision, prev_ext_service_cost_dict, True, True, new_line_name='ext_prev_cost', url_viewset='/suivi_budg/table_budgetaire/')


        # filtrons pour  Intern spendings (Prestation externes achats)
        prev_intern_spend_cost_filt = prev_cost.filter(type__type='SP_I')
        prev_intern_spend_cost_dict = prev_intern_spend_cost_filt.values('pk', 'titled','amount')
        for l in prev_intern_spend_cost_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']
        # creons la bd pour les prestations externes prevision
        data1['prev_intern_spend_cost'] = create_dict_with_data('recap_recettes',col_prevision, prev_intern_spend_cost_dict, True, True, new_line_name='intern_spend_prev', url_viewset='/suivi_budg/table_budgetaire/')


        '''
        FIN CHANGING VALUE test
        '''

        #       --------------------       ---------------------           -------------------    #
        #Creating the basics for Recettes tables (prevision or reel)
        # Prestation previsionel, calling the data
        prestations_vents_recettes_int = PrestationsVentsRecettesInt.objects.all()

        # créons le liste avec les prestations prevision recettes
        recette_presta_prev_filt = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='P')
        recette_presta_prev_dict = recette_presta_prev_filt.values('pk', 'date','amount')
        for l in recette_presta_prev_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']
        # creons la bd pour les prestations externes prevision
        data1['recette_presta_prev'] = create_dict_with_data('recap_recettes',col_prevision, recette_presta_prev_dict, True, True, new_line_name='new_recette_1_prev', url_viewset='/suivi_budg/table_budgetaire/')

        # créons le liste avec les ventes prevision recettes
        vents_recett_prev = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='V')
        data0['vents_recett_prev'] = create_dict_with_data('recap_recettes',col_prevision, vents_recett_prev, True, True)

        # créons le liste avec les recettes int prev
        intern_recett_prev = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='R_IN')
        data0['intern_recett_prev'] = create_dict_with_data('recap_recettes',col_prevision, intern_recett_prev, True, True)

        '''
            END OF TESTING OTHER KIND OF TEMPLATE

        '''

        # ajoutons les depenses réeles internes
        # Nous devrons tout d'abourd ajouter une nouvelle variable colones basé
        # sur les colone previsions
        col_with_date_amaunt = [
        {'nom':'','list': True},
        {'nom':'date', 'date': True, 'total': False},
        {'nom':'amount', 'input': True},
        {'nom':'', 'input': False},
        {'nom':'', 'input': False}
        ]


        # créons le liste filtre avec les depenses internes reel
        depenses_int_real_filt = RealCostInternSpending.objects.filter(type__type='SP_I')
        depenses_int_real_dict = depenses_int_real_filt.values('pk', 'date_cost','pole_id', 'amount')
        # Add edit and efface  butons
        for l in depenses_int_real_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']

        # creons la bd pour les prestations internne prevision
        data1['depenses_int_reel'] = create_dict_with_data('recap_recettes',col_with_date_amaunt, depenses_int_real_dict, True, True, new_line_name='new_line_prev_cost', url_viewset='/suivi_budg/table_budgetaire/')


        # On va recupperer les données de coûts reels
        # pour les filtrer par la suite
        real_cost = RealCost.objects.all()

        real_cost_ser = RealcostSerializer(data=request.GET)
        # filter on Caring
        real_cost_caring_filt = real_cost.filter(type__type='CAR')

        # let's create the dictionary
        real_cost_caring_dict = real_cost_caring_filt.values('pk','user_id','date','proposition','validated', 'invoiced','paid')
            # using the annotate method
            #annotate.username=F('user__username'))
        for l in real_cost_caring_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']


        col_dep_reel = [
                {'nom':''}, #les bienveillants peuvent selectionné un nom si il créé une nouvelle ligne
                {'nom':'date', 'input': True, 'total': False}, #les bienveillants peuvent remplir une date
                {'nom':'propo.' , 'input': True}, #les bienveillants peuvent remplir un un amount
                {'nom':'validé', 'input': True}, #les bienveillants peuvent valider
                {'nom':'factu.', 'input': True}, #les bienveillants peuvent valider
                {'nom':'payé'}, #si la facture est "payé" dans odoo, la checkbox est True, il y aura un peu de réflexion à avoir pour voir comment associé une proposition à une facture odoo
                {'nom':'', 'input': False},
                {'nom':'', 'input': False},

        ]
        # Creons le Bd pour la bienveillance reel

        # creons la bd pour les prestations externes prevision
        data1['bienveillance_reel'] = create_dict_with_data('recap_recettes',col_dep_reel, real_cost_caring_dict, True, True, new_line_name='new_recette_1_prev', url_viewset='/suivi_budg/table_budgetaire/')


        # Creaons une liste des données qu'on va afficher dans le table
        # presta interne reel
        presta_int_reel_filt = real_cost.filter(type__type='IN_S')
        presta_int_reel_dict = presta_int_reel_filt.values('pk','date','proposition','validated', 'paid','proposition')

        # Add edit and efface  butons
        for l in presta_int_reel_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']

        # creons la Bd pour presta intern reel
        data1['presta_int_reel'] = create_dict_with_data('recap_recettes',col_dep_reel, presta_int_reel_dict, True, True, new_line_name='new_recette_1_prev', url_viewset='/suivi_budg/table_budgetaire/')

        # Creons colonnes pour dépenses externes réels
        col_dep_reel_ext = [
                {'nom':''},  #le nom des facture de tout les articles sauf co-rem et presta int
                {'nom':'intitulé'}, #l'intitulé des facture
                {'nom':'date', 'total': False}, #date des factures
                {'nom':'validé',},#si la facture est "validé" dans odoo, la checkbox est True, c'est une checkbox non modifiable par l'utilisateur
                {'nom':'payé',}, #si la facture est "payé" dans odoo, la checkbox est True, c'est une checkbox non modifiable par l'utilisateur
                {'nom':'', 'input': False},
                {'nom':'', 'input': False}
            ]
        # applons la bd des prestations externes reeles
        presta_ext_reel0 = RealCostExternService.objects.all()

        # depense reel exterieur
        presta_ext_reel_dict = presta_ext_reel0.values('pk','titled','date','validated', 'payed')

        # Add edit and efface  butons
        for l in presta_ext_reel_dict:
            l['edit'] = l['pk']
            l['efface'] = l['pk']

        data1['presta_ext_reel'] = create_dict_with_data('recap_recettes',col_dep_reel_ext, presta_ext_reel_dict, True, True, new_line_name='new_recette_1_prev', url_viewset='/suivi_budg/table_budgetaire/')


        #Creating the basics for Recettes tables (prevision or reel)
        # Prestation previsionel, calling the data

        # Recettes reeles
        # créons le bd avec les recettes presta intern
        presta_recett_reel = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='R_IN')
        data0['presta_recett_reel'] = create_dict_with_data('recap_recettes',col_prevision, presta_recett_reel, True, True)

        # Ventes reeles recettes
        recettes_vents_reel = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='R_IN')
        data0['recettes_vents_reel'] = create_dict_with_data('recap_recettes',col_prevision, recettes_vents_reel, True, True)

        # recettes internes reeles
        recettes_int_reel = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='R_IN')
        data0['recettes_int_reel'] = create_dict_with_data('recap_recettes',col_prevision, recettes_int_reel, True, True)

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = {
            'base_template': base_template,
            'data1': data1,
            'data0': data0
        }

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html', context=context)

    # creating budget cost
    def create(self, request):
        "Controleur pour POST"
        serializer = PrevisionCostSerializer(data=request.data)
        # searching
        serializer_recettes = PrestationsVentsRecettesIntValidator(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return render(request, 'dashboard/pages_html/suivi_budgetaire.html')


    # updating budget cost
    def update(self, request, pk=None):
        "Controleur pour PUT"
        pass


    # deleting budget cost
    def destroy(self, request, pk=None):
        "Controleur pour DELETE"
        all_objects = PrevisionCost.objects.all()
        obj = get_object_or_404(all_objects, pk=pk)
        obj.delete()
        return redirect('/suivi_budg/table_budgetaire/')



# class viewset for organigramme
class OrganizationalChartViewSet(viewsets.ViewSet):

    # method for listing organigramme
    def list(self, request):
        data1 = {}
        # creating colones
        col_org = [
            {'nom': '', 'list': True},
            {'nom': 'presta interne', 'input': True},
            {'nom': 'garant du cadre', 'input': True},
            {'nom': 'référent budgt / subvention', 'input': True},
            {'nom': 'référent tâche planning', 'input': True},
            {'nom': '', 'input': False},
            {'nom':'', 'input': False}
        ]
        # Creer la liste avec les données de l'organigrame
        organigramme_list = [[{'pk':x.pk},{'user_name':x.user.name}, {'intern_services': x.intern_services}, {'settlement_agent': x.settlement_agent}, {'budget_referee': x.budget_referee}, {'task_planning_referee': x.task_planning_referee}] for x in OrganizationalChart.objects.all()]
        edit_efface(organigramme_list)

        data1['organigramme'] = create_dict_with_data('organigramme_new', col_org, organigramme_list, False, True,new_line_name='organigramme_new')
        # adding the url that will be used to add, create or edit OragnizationalChart objects
        data1['organigramme']['crud_url'] = '/suivi_budg/organizationalchart/'

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = {
            'base_template': base_template,
            'data1': data1,
        }

        return render(request, 'dashboard/pages_html/organigramme.html', context=context)


    # method for creating organigramme
    def create(self, request):
        "Controleur pour POST"
        # Reciving data from new line and creating a new personne on organigramme
        serializer = OrganizationalChartValidator(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return redirect('/suivi_budg/organizationalchart/')


    # Delete organizationalchart object
    def destroy(self, request, pk=None):
        "Controleur pour DELETE"
        if request.method == 'DELETE':# and request.POST.get('_method') == 'DELETE':
            all_objects = OrganizationalChart.objects.all()
            obj = get_object_or_404(all_objects, pk=pk)
            obj.delete()
            return redirect('/suivi_budg/organizationalchart/')

        # return redirect('/suivi_budg/organizationalchart/')


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



def organigramme(request):
    dataO = {}
    # creating colones
    col_org = [
        {'nom':'', 'list': True},
                    {'nom':'presta interne', 'input': True},
                    {'nom':'garant du cadre', 'input': True},
                    {'nom':'référent budgt / subvention', 'input': True},
                    {'nom':'référent tâche planning', 'input': True}
    ]
    # Creer la liste avec les données de l'organigrame
    organigramme_list = [[x.user.name, x.intern_services, x.settlement_agent, x.budget_referee, x.task_planning_referee] for x in OrganizationalChart.objects.all()]
    dataO['organigramme'] = create_dict_with_data('organigramme_new', col_org, organigramme_list, False, True,new_line_name='organigramme_new')

    #Reciving data from new line and creating a new personne on organigramme
    if request.method == 'POST':

        # serch the validated data from serializer for the new line
        new_organigramme_validator = OrganizationalChartValidator(data=request.POST)

        if not new_organigramme_validator.is_valid():
            base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
            return render(request, 'dashboard/pages_html/organigramme.html', {'message_org_new': "Le nom choisit il existe déjà dans l'organigramme", 'base_template': base_template})

        validated_data_org = new_organigramme_validator.validated_data

        user_pk = validated_data_org.get('users').pk
        user = CustomUser.objects.get(pk=user_pk)
        # Attention if you do validated_data_org['intern_services'] it will search
        # a key that doesn't exist and will return error in case the checkbox isn't
        # 'on' if you do var_validated.get('name') it will search vor the name and
        # won't return an error.
        def refacto_check_var(var):
            return True if validated_data_org.get(var) == 'check' else False

        intern_services= refacto_check_var('intern_services')
        settlement_agent= refacto_check_var('settlement_agent')
        budget_referee= refacto_check_var('budget_referee')
        task_planning_referee = refacto_check_var('task_planning_referee')

        user_choice = CustomUser.objects.get(username=user)

        OrganizationalChart.objects.create(user=user_choice,
                                           intern_services=intern_services,
                                           settlement_agent=settlement_agent,
                                           budget_referee=budget_referee,
                                           task_planning_referee=task_planning_referee
                                           )
        return redirect('organigramme')


    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,
        'data': data,
        'dataO': dataO,
    }

    return render(request, 'dashboard/pages_html/organigramme.html', context=context)


'''
Sending data to the forms of nwe line in Prevision Cost tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''
# ------------ Start
# send data to Caring (bienveillance) form

def caring_data_form(request):
    cost_type = Cost.objects.get(type='CAR')

    return render(request, 'new_lines/new_budget_cost_prev.html', {'cost_type': cost_type})


# send data to intern prevision cost form
def intern_serv_prev_form(request):
    cost_type = Cost.objects.get(type='IN_S')

    return render(request, 'new_lines/new_budget_cost_prev.html', {'cost_type': cost_type})


# send data to extern prevision cost form
def ext_serv_prev_form(request):
    cost_type = Cost.objects.get(type='EX_S')

    return render(request, 'new_lines/new_budget_cost_prev.html', {'cost_type': cost_type})

# send data to intern spendings cost form
def intern_spend_prev_form(request):
    cost_type = Cost.objects.get(type='SP_I')

    return render(request, 'new_lines/new_budget_cost_prev.html', {'cost_type': cost_type})

#---------------- FIN FORM NEW LINE PREV COST --------


'''
Sending data to the forms of nwe line in RECETTES tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''
# ------------ Start

# form for Prestation prevision
def recette_form_prev_1(request):
    recette = Recette.objects.get(type='P') # SUB   v   RIN
    prev_ou_reel = 'P'
    return render(request, 'new_lines/new_line_recettes.html', {'recette': recette, 'prev_ou_reel': prev_ou_reel })




#---------------- FIN FORM NEW LINE RECETTES --------



# send user to organigrame creating new line
def send_user_to_organigrame(request):
    all_users = CustomUser.objects.all()

    return render(request, 'htmx/new_organigramme.html', {'user':all_users})


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
    
