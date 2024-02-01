from django.core.management.base import BaseCommand, CommandError
from dashboard_app.models import Group, Pole, Cost, PrevisionCost, RealCost, RealCostExternService, RealCostInternSpending


# Creating the bases of Groupe db
def create_groupes():
    groupes = [
        {'name': 'Les communs', 'code': '10', 'user': 'Steph'},
        {'name': 'Les communs', 'code': '10', 'user': 'Céline'},
        {'name': 'Alimentation', 'code': '20', 'user': 'Céline'},
        {'name': 'Jardin', 'code': '30', 'user': 'Stiff'},
        {'name': 'Micro-Recylerie', 'code': '40', 'user': 'Julien'},
        {'name': 'Culture', 'code': '50', 'user': 'Laetitia'},
        {'name': 'Services', 'code': '70', 'user': 'Guillaume B'},
    ]

    # creating all groupes with a loop
    for groupe in groupes:
        gr, creted = Group.objects.get_or_create(**groupe)

# Creating the bases of pole db
def create_poles():
    poles = [
        {'name': 'Interpôle', 'code': '2', 'type': Pole.POLE, 'user': 'Steph','groupe': Group.objects.get(name='Les communs',user__username = 'Stiff')},
        {'name': 'Outils communs', 'code': '3', 'type': Pole.POLE, 'user': 'Céline','groupe': Group.objects.get(name='Les communs',user__username = 'Céline')},
        {'name': 'Instances', 'code': '4', 'type': Pole.POLE, 'user': 'Céline','groupe': Group.objects.get(name='Les communs',user__username = 'Céline')},
        {'name': 'Snack / Bar', 'code': '2', 'type': Pole.GROUP, 'user': 'Céline','groupe': Group.objects.get(name='Alimentation',user__username = 'Céline')},
        {'name': 'Micro-forêt', 'code': '2', 'type': Pole.POLE, 'user': 'Anouk','groupe': Group.objects.get(name='Jardin',user__username = 'Stiff')},
        {'name': 'Potager', 'code': '3', 'type': Pole.POLE, 'user': 'Stiff','groupe': Group.objects.get(name='Jardin', user__username = 'Stiff')},
        {'name': 'Serre aquaponique', 'code': '4', 'type': Pole.POLE, 'user': 'Stiff','groupe': Group.objects.get(name='Jardin', user__username ='Stiff')},
        {'name': 'Champignonnière', 'code': '5', 'type': Pole.POLE, 'user': 'Stiff','groupe': Group.objects.get(name='Jardin', user__username ='Stiff')},
        {'name': 'Café culturel', 'code': '3', 'type': Pole.POLE, 'user': 'Laetitia','groupe': Group.objects.get(name='Culture', user__username ='Laetitia')},
        {'name': 'Culture Lab', 'code': '2', 'type': Pole.POLE, 'user': 'Laetitia','groupe': Group.objects.get(name='Culture', user__username ='Laetitia')},
    ]

    # creating all poles with a loop
    for pole in poles:
        pl, creted = Pole.objects.get_or_create(**pole)



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
        {'type': Cost.objects.get(type=Cost.INTERN_SERVICE), 'titled': 'animation'},
        {'type': Cost.objects.get(type=Cost.INTERN_SERVICE), 'titled': 'entretien matérie'},
        {'type': Cost.objects.get(type=Cost.EXTERN_SERVICE), 'titled': 'matériel'},
        {'type': Cost.objects.get(type=Cost.EXTERN_SERVICE), 'titled': 'consomable'},
        {'type': Cost.objects.get(type=Cost.INTERN_SPENDS), 'titled': 'consomable'},
        {'type': Cost.objects.get(type=Cost.INTERN_SPENDS), 'titled': 'consomable'}
    ]
    for prevision in previsions:
        prev, created = PrevisionCost.objects.get_or_create(**prevision)
