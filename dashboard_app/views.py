import time

from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import format_html
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboard_app.data import data
from dashboard_user.models import CustomUser
from .models import PrevisionCost
from dashboard_app.models import (Contact, AccountAccount, AccountJournal, AccountAnalyticGroup, AccountAnalyticAccount, \
    RealCostInternSpending, RealCost, RealCostExternService, PrestationsVentsRecettesInt, Grant, Cost,
    OrganizationalChart, Badge, DepensesBienveillance)
from dashboard_app.odoo_api import OdooApi
from dashboard_app.serializers import UserSerializer
from .serializers import (AccountAnalyticGroupSerializer, OrganizationalChartValidator,
                PrestationsVentsRecettesIntValidator, PrevisionCostValidator)
from dashboard_app.models import AccountAccount

# We'll create a fonction that will return a dictionary in the form adapted to
# the generale tables
def create_dict_with_data(slug_name, colonnes,lignes, total,new_ligne,new_line_name="",titre_colonne=""):

    return {
        "slug": slug_name,
        "titre": titre_colonne,
        "colonnes": colonnes,
        "lignes": lignes,
        "total": total,
        "ajouter_ligne" : new_ligne,
        'new_line_name': new_line_name
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


# Add edit and efface  buton lines
def edit_efface(list): # A ajoutter dans la classe SuviBudgetaireViewSet
    for l in list:
        l.append({'edit': l[0]['pk']})
        l.append({'efface': l[0]['pk']})

def add_buttons(list): # A ajoutter dans la classe SuviBudgetaireViewSet
    for l in list:
        l.append('edit')
        l.append('efface')

# suivi budgetaire with Vieset
class SuiviBudgetaireViewSet(viewsets.ViewSet):
    def list(self, request):
        "Controleur pour GET"

        '''
            TESTING OTHER KIND OF TEMPLATE
        '''
        # the data0 dictionary will serve gatherign data of different cases
        data0 = {}

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
        prev_cost_caring = prev_cost.filter(type__type='CAR')
        # creons la bd pour bienveillance prevision
        data0['prev_cost_caring'] = create_dict_with_data( "prev_beinveillance", col_prevision,prev_cost_caring, True, True, new_line_name='new_prev_bienveillance')


        # filtrons pour  Interne services (Prestation internes)
        prev_intern_service_cost = prev_cost.filter(type__type='IN_S')
        data0['prev_intern_service_cost'] = create_dict_with_data('prev_intern_serv',col_prevision, prev_intern_service_cost, True, True, new_line_name='int_serv_prev')


        # filtrons pour  Extern service (Prestation externes achats)
        prev_ext_service_cost = prev_cost.filter(type__type='EX_S')

        # creons la bd pour les prestations externes prevision
        data0['prev_ext_service_cost'] = create_dict_with_data('recap_recettes',col_prevision, prev_ext_service_cost, True, True)


        # filtrons pour  Intern spendings (Prestation externes achats)
        prev_intern_spend_cost = prev_cost.filter(type__type='SP_I')
        # creons la bd pour les prestations externes prevision
        data0['prev_intern_spend_cost'] = create_dict_with_data('recap_recettes',col_prevision, prev_intern_spend_cost, True, True)


        #       --------------------       ---------------------           -------------------    #
        #Creating the basics for Recettes tables (prevision or reel)
        # Prestation previsionel, calling the data
        prestations_vents_recettes_int = PrestationsVentsRecettesInt.objects.all()

        # créons le liste avec les prestations prevision
        # créons le liste avec les prestations prevision recettes
        recette_presta_prev = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='P')
        data0['recette_presta_prev'] = create_dict_with_data('recap_recettes',col_prevision, recette_presta_prev, True, True, )

        # créons le liste avec les ventes prevision recettes
        vents_recett_prev = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='V')
        data0['vents_recett_prev'] = create_dict_with_data('recap_recettes',col_prevision, vents_recett_prev, True, True)

        # créons le liste avec les recettes int prev
        intern_recett_prev = prestations_vents_recettes_int.filter(prev_ou_reel='P', recette__type='R_IN')
        data0['intern_recett_prev'] = create_dict_with_data('recap_recettes',col_prevision, intern_recett_prev, True, True)

        data1 = {}
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
        # creons une liste pour les presta externs prevision
        depenses_int_real_list = [[{'pk':x.pk}, {'pole_id': x.pole.name}, {'date': str(x.date_cost)}, {'amount': str(x.amount)}] for x in RealCostInternSpending.objects.filter(type__type='SP_I')]
        # Add edit and efface  butons
        edit_efface(depenses_int_real_list)

        # creons la bd pour les prestations externes prevision
        data1['depenses_int_reel'] = create_dict_with_data('recap_recettes',col_with_date_amaunt, depenses_int_real_list, True, True)

        # On va recupperer les données de coûts reels
        # pour les filtrer par la suite
        real_cost = RealCost.objects.all()
        # Creaons une liste des données qu'on va afficher dans le table
        # bienveillance réel
        bienveillance_reel_list = [[{'pk':x.pk},{'username':x.user.username}, {'date': x.date}, {'proposition': str(x.proposition)}, {'validated': x.validated}, {'invoiced': x.invoiced}, {'paid': x.paid}] for x in real_cost.filter(type__type='CAR')]

        # Add edit and efface  butons
        edit_efface(bienveillance_reel_list)

        col_dep_reel = [
                {'nom':''}, #les bienveillants peuvent selectionné un nom si il créé une nouvelle ligne
                {'nom':'date', 'input': True, 'total': False}, #les bienveillants peuvent remplir une date
                {'nom':'propo.' , 'input': True}, #les bienveillants peuvent remplir un un amount
                {'nom':'validé', 'input': True}, #les bienveillants peuvent valider
                {'nom':'factu.', 'input': True}, #les bienveillants peuvent valider
                {'nom':'payé'}, #si la facture est "payé" dans odoo, la checkbox est True, il y aura un peu de réflexion à avoir pour voir comment associé une proposition à une facture odoo
                {'nom':'', 'input': False},
                {'nom':'', 'input': False}
        ]
        # Creons le Bd pour la bienveillance reel
        data1['bienveillance_reel'] = create_dict_with_data('recap_recettes',col_dep_reel, bienveillance_reel_list, True, True)

        # Creaons une liste des données qu'on va afficher dans le table
        # presta interne reel
        presta_int_reel_list = [[{'pk':x.pk},{'username':x.user.username}, {'date': x.date}, {'proposition': str(x.proposition)}, {'validated': x.validated}, {'invoiced': x.invoiced}, {'paid': x.paid}] for x in real_cost.filter(type__type='IN_S')]

        # Add edit and efface  butons
        edit_efface(presta_int_reel_list)

        # creons la Bd pour presta intern reel
        data1['presta_int_reel'] = create_dict_with_data('recap_recettes',col_dep_reel, presta_int_reel_list, True, True)

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
        real_cost_spendings = RealCostExternService.objects.all()

        #créons la liste avec les dépenses externes réeles
        presta_ext_reel_list = [[{'pk':x.pk},{'contact_name':x.contact.name}, {'titled': x.titled}, {'date': x.date}, {'validated': x.validated}, {'payed': x.payed}] for x in real_cost_spendings]
        # Add edit and efface  butons
        edit_efface(presta_ext_reel_list)

        data1['presta_ext_reel'] = create_dict_with_data('recap_recettes',col_dep_reel_ext, presta_ext_reel_list, True, True)

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
        serializer = PrevisionCostValidator(data=request.data)
        # searching
        serializer_recettes = PrestationsVentsRecettesIntValidator(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return redirect('/suivi_budg/table_budgetaire/')

        # creating PrestationsVentsRecettesInt
        if serializer_recettes.is_valid():
            serializer_recettes.save()

        return redirect('/suivi_budg/table_budgetaire/')



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

# Creating the options for new line in a generic html doc
def new_line_cost(request):
    data2 = {}
    prevision_cost = PrevisionCost.objects.all()
    # adding the type to the data for the caring case
    type = prevision_cost.filter(type__type='CAR').first()
    id = 'prev_caring'
    data2['prev_caring'] = {'type_id': type.pk, 'id': id}

    # adding the type to the data for the Internal service case case
    type = prevision_cost.filter(type__type='IN_S').first()
    id = 'prev_intern_service'
    data2['prev_intern_services'] = {'type_id': type.pk, 'id': id}

    # adding the type to the data for the External service case case
    type = prevision_cost.filter(type__type='EX_S').first()
    id = 'prev_external_service'
    data2['prev_ext_serv_purchase'] = {'type_id': type.pk, 'id': id}


    # adding the type to the data for the Internal spendings (dépenses internes) case
    type = prevision_cost.filter(type__type='SP_I').first()
    id = 'prev_intern_spendings'
    data2['prev_intern_spendings'] = {'type_id': type.pk, 'id': id}

    context= {
        'data2': data2
    }

    return render(request, 'new_lines/new_line_cost.html', context=context)


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


# send data to Caring (bienveillance) form
def caring_data_form(request):
    cost_caring = Cost.objects.get(type='CAR')

    return render(request, 'htmx/new_budget_cost.html', {'cost_caring': cost_caring})


# send data to intern prevision cost form
def intern_serv_prev_form(request):
    intern_service = Cost.objects.get(type='IN_S')

    return render(request, 'htmx/new_prev_cost_intern.html', {'intern_service': intern_service})


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
    
