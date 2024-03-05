from rest_framework import serializers

from dashboard_user.models import CustomUser
from .models import (AccountAccount, AccountAnalyticGroup, PrevisionCost, OrganizationalChart,
                     PrestationsVentsRecettesInt, RealCost)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid',
            'email',
        ]
        read_only_fields = ('uuid', 'email',)


# Validator for OrganizationalChart
class OrganizationalChartValidator(serializers.ModelSerializer):
    class Meta:
        model = OrganizationalChart

        fields = ['user', 'intern_services', 'settlement_agent', 'budget_referee', 'task_planning_referee']



# Validator for previzion budget
class PrevisionCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrevisionCost
        fields = ['titled', 'amount','type', 'pk']


# VAlidator for PrestationsVentsRecettesInt
class PrestationsVentsRecettesIntValidator(serializers.ModelSerializer):
    class Meta:
        model = PrestationsVentsRecettesInt
        fields = ['date', 'amount', 'pk']


class RealcostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = RealCost
        fields = ['user','username', 'date', 'proposition', 'validated', 'invoiced','paid', 'type', 'pk' ]

    def get_username(self, obj):
        return obj.user.username

    # Geting the checkbox values in false when it's not checked
    def to_internal_value(self, data):
        # Provide default values for unchecked checkboxes
        data.setdefault('validated', False)
        data.setdefault('invoiced', False)
        data.setdefault('paid', False)
        return super().to_internal_value(data)


class AccountAnalyticGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAnalyticGroup
        fields = [
            'uuid',
            'name',
            'id_odoo',
        ]

class AccountAnalyticGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAnalyticGroup
        fields = [
            'uuid',
            'name',
            'id_odoo',
        ]



# class PrevisionCostSerializer(serializers.Serializer):
#     # amount = serializers.DecimalField()
#     # titled = serializers.DecimalField()
#
#
#     def dictionary_with_prevision_cost(self):
#         prevision_costs = PrevisionCost.objects.filter(type__type='CAR')
#         titled = prevision_costs.titled
#         amount = prevision_costs.amount
#         bienveillance_prev = {
#             "slug": "recap_recettes",
#             "titre": "",
#             "colonnes": [
#                 {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés
#                 {'nom':'amount', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants
#             ],
#             "lignes": [titled,amount],
#             "total":True
#         }
#         return
