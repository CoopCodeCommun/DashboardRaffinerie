from django.core.management.base import BaseCommand, CommandError
from dashboard_app.models import Groupe, Pole, Cost, PrevisionCost, RealCost, RealCostExternService, RealCostInternSpending
from dashboard_user.models import CustomUser, ContactProvisional
from time import timezone
import uuid


# creating provisoire users
def create_prov_user():
    users = [
        {'email': 'julien@laraffinerie.re', 'name': 'Julien', 'username': 'Julien','type': CustomUser.BENEFICIEAIRE},
        {'email': 'steph@laraffinerie.re', 'name': 'Steph', 'username': 'Steph','type': CustomUser.BENEFICIEAIRE},
        {'email': 'stiff@laraffinerie.re', 'name': 'Stiff', 'username': 'Stiff','type': CustomUser.BENEFICIEAIRE},
        {'email': 'celine@laraffinerie.re', 'name': 'Céline', 'username': 'Céline','type': CustomUser.BENEFICIEAIRE},
        {'email': 'laetitia@laraffinerie.re', 'name': 'Laetitia', 'username': 'Laetitia','type': CustomUser.BENEFICIEAIRE},
        {'email': 'guillaume.b@laraffinerie.re', 'name': 'Guillaume B', 'username': 'Guillaume B','type': CustomUser.BENEFICIEAIRE},
        {'email': 'tim@laraffinerie.re', 'name': 'Tim', 'username': 'Tim','type': CustomUser.BENEFICIEAIRE},
        {'email': 'antoine@laraffinerie.re', 'name': 'Antoine', 'username': 'Antoine','type': CustomUser.BENEFICIEAIRE},
        {'email': 'claire@laraffinerie.re', 'name': 'Claire', 'username': 'Claire','type': CustomUser.BENEFICIEAIRE},
        {'email': 'flore@laraffinerie.re', 'name': 'Flore', 'username': 'Flore','type': CustomUser.BENEFICIEAIRE},
        {'email': 'anouk@laraffinerie.re', 'name': 'Anouk', 'username': 'Anouk','type': CustomUser.BENEFICIEAIRE},
        {'email': 'manon.g@laraffinerie.re', 'name': 'Manon G', 'username': 'Manon G','type': CustomUser.BENEFICIEAIRE},
        {'email': 'france@laraffinerie.re', 'name': 'France', 'username': 'France','type': CustomUser.BENEFICIEAIRE},
        {'email': 'remy@laraffinerie.re', 'name': 'Remy', 'username': 'Remy','type': CustomUser.USER_QONTO},
        {'email': 'georgete@laraffinerie.re', 'name': 'Georgette', 'username': 'Georgette','type': CustomUser.USER_QONTO},
        {'email': 'huges@laraffinerie.re', 'name': 'Huges', 'username': 'Huges','type': CustomUser.USER_QONTO},
        {'email': 'yvette@laraffinerie.re', 'name': 'Yvette', 'username': 'Yvette','type': CustomUser.USER_QONTO},
    ]

    dict_users = {}
    #loop to create the users:
    for user in users:
        usr, created = CustomUser.objects.get_or_create(**user)
        dict_users[usr.name] = usr

    # Return the dictionair with the user object
    return dict_users

# creating some provisoil contacts
def create_contacts():
    ContactProvisional.objects.get_or_create(email='vents@ravate.re', name='Ravate')
    ContactProvisional.objects.get_or_create(email='vents@decathlon.re', name='Decathlon')

# Creating the bases of Groupe db
def create_groupes(dict_users):
    # create a dictionair so we can regroupe all group objects with their name as key
    group_dict = {}
    #creating groups with one users or multiple users (many to many)
    gr, created = Groupe.objects.get_or_create(name='Les communs', code= 10)
    gr.users.add(dict_users['Céline'])
    gr.users.add(dict_users['Steph'])
    group_dict[gr.name] = gr.pk
    gr2, created = Groupe.objects.get_or_create(name='Alimentation', code= 20)
    gr2.users.add(create_prov_user()['Céline'])
    group_dict[gr2.name] = gr2.pk
    gr3, created = Groupe.objects.get_or_create(name='Jardin', code= 30)
    gr3.users.add(dict_users['Stiff'])
    group_dict[gr3.name] = gr3.pk
    gr4, created = Groupe.objects.get_or_create(name='Micro-Recylerie', code= 40)
    gr4.users.add(dict_users['Julien'])
    group_dict[gr4.name] = gr4.pk
    gr5, created = Groupe.objects.get_or_create(name='Culture', code= 50)
    gr5.users.add(dict_users['Laetitia'])
    group_dict[gr5.name] = gr5.pk
    gr6, created = Groupe.objects.get_or_create(name='Services', code= 70)
    gr6.users.add(dict_users['Guillaume B'])
    group_dict[gr6.name] = gr6.pk

    return group_dict

# Creating the bases of pole db
def create_poles(dict_user, group_pk_dict):
    dict_pk_pol = {}
    pol0, created = Pole.objects.get_or_create(name='Interpole', code= 2, user=dict_user['Steph'], group_id=group_pk_dict['Les communs'])
    dict_pk_pol[pol0.name] = pol0.pk

    pol1, created = Pole.objects.get_or_create(name='Outils communs', code= 3, user=dict_user['Céline'], group_id=group_pk_dict['Les communs'])
    dict_pk_pol[pol1.name] = pol1.pk

    pol2, created = Pole.objects.get_or_create(name='Instances', code= 4, user=dict_user['Steph'], group_id=group_pk_dict['Les communs'])
    dict_pk_pol[pol2.name] = pol2.pk

    pol3, created = Pole.objects.get_or_create(name='Snack / Bar', code= 2, user=dict_user['Céline'], group_id=group_pk_dict['Alimentation'])
    dict_pk_pol[pol3.name] = pol3.pk

    pol4, created = Pole.objects.get_or_create(name='Micro-forêt', code= 2, user=dict_user['Steph'], group_id=group_pk_dict['Jardin'])
    dict_pk_pol[pol4.name] = pol4.pk

    pol5, created = Pole.objects.get_or_create(name='Potager', code= 3, user=dict_user['Céline'], group_id=group_pk_dict['Jardin'])
    dict_pk_pol[pol5.name] = pol5.pk

    pol6, created = Pole.objects.get_or_create(name='Serre aquaponique', code= 4, user=dict_user['Steph'], group_id=group_pk_dict['Jardin'])
    dict_pk_pol[pol6.name] = pol6.pk

    pol7, created = Pole.objects.get_or_create(name='Champignonnière', code= 5, user=dict_user['Céline'], group_id=group_pk_dict['Jardin'])
    dict_pk_pol[pol7.name] = pol7.pk

    pol8, created = Pole.objects.get_or_create(name='Café culturel', code= 3, user=dict_user['Steph'], group_id=group_pk_dict['Culture'])
    dict_pk_pol[pol8.name] = pol8.pk

    pol9, created = Pole.objects.get_or_create(name='Culture Lab', code= 2, user=dict_user['Céline'], group_id=group_pk_dict['Culture'])
    dict_pk_pol[pol0.name] = pol9.pk

    return dict_pk_pol

# Creating cost base db
def cost_base():
    for i in range(8):
        Cost.objects.get_or_create(type=Cost.CARING)
        Cost.objects.get_or_create(type=Cost.INTERN_SERVICE)
        Cost.objects.get_or_create(type=Cost.EXTERN_SERVICE)
        Cost.objects.get_or_create(type=Cost.INTERN_SPENDS)
        Cost.objects.get_or_create(type=Cost.SUBVENTION)
        Cost.objects.get_or_create(type=Cost.SERVICE)
        Cost.objects.get_or_create(type=Cost.SELL)
        Cost.objects.get_or_create(type=Cost.INTERN_RECIPE)


# Creating prevision cost db
def prevision_cost():
    previsions = [
        {'type': Cost.objects.get(type=Cost.CARING), 'titled': 'garant du cadre'},
        {'type': Cost.objects.get(type=Cost.CARING),'titled': 'ref budget'},
        {'type': Cost.objects.get(type=Cost.CARING),'titled': 'ref communication'},
        {'type': Cost.objects.get(type=Cost.INTERN_SERVICE), 'titled': 'animation'},
        {'type': Cost.objects.get(type=Cost.INTERN_SERVICE), 'titled': 'entretien matérie'},
        {'type': Cost.objects.get(type=Cost.EXTERN_SERVICE), 'titled': 'matériel'},
        {'type': Cost.objects.get(type=Cost.EXTERN_SERVICE), 'titled': 'consomable'},
        {'type': Cost.objects.get(type=Cost.INTERN_SPENDS), 'titled': 'micro-recylerie'},
        {'type': Cost.objects.get(type=Cost.INTERN_SPENDS), 'titled': 'culture'},
        {'type': Cost.objects.get(type=Cost.INTERN_SPENDS), 'titled': 'commun'}
    ]
    for prevision in previsions:
        prev, created = PrevisionCost.objects.get_or_create(**prevision)


# Create db for interne cost real
def intern_real_cost(dict_pole_pk):
    intern_spend_real, created = RealCostInternSpending.objects.get_or_create(type=Cost.INTERN_SPENDS, pole_id= dict_pole_pk['Café culturel'])
    intern_spend_real, created = RealCostInternSpending.objects.get_or_create(type=Cost.INTERN_SPENDS, pole_id= dict_pole_pk['Micro-forêt'])


# deleting all the db
def delete_models():
    CustomUser.objects.all().delete()
    ContactProvisional.objects.all().delete()
    Groupe.objects.all().delete()
    Pole.objects.all().delete()
    Cost.objects.all().delete()
    PrevisionCost.objects.all().delete()


# BaseCommand to create DB
class Command(BaseCommand):
    def handle(self, *args, **options):
        # create the users and collect the user objects in a dictionary
        dict_user = create_prov_user()
        create_contacts()
        # create the groups and collect the group objects in a dictionary
        group_dict = create_groupes(dict_user)
        poles_pk = create_poles(dict_user, group_dict)
        # creating Cost basic elements
        cost_base()
        # creating prevision cost
        prevision_cost()
        #import ipdb; ipdb.set_trace()
        # creating real intern cost
        intern_real_cost(poles_pk)


        #delete_models()
