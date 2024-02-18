from rest_framework import serializers

from dashboard_user.models import CustomUser
from .models import AccountAccount, AccountAnalyticGroup, PrevisionCost, OrganizationalChart


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

    '''
    
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    intern_services = serializers.CharField(required=False, allow_null=True)
    settlement_agent = serializers.CharField(required=False, allow_null=True)
    budget_referee = serializers.CharField(required=False, allow_null=True)
    task_planning_referee = serializers.CharField(required=False, allow_null=True)

    # Validate the intern_service checkbox send True if is checked or false in not
    def validate_intern_services(self, value):
        if value == 'check':
            return value

    # Validate the settlement_agent checkbox send True if is checked or false in not
    def validate_settlement_agent(self, value):
        if value == 'check':
            return value

    # Validate the budget_referee checkbox send True if is checked or false in not
    def validate_budget_referee(self, value):
        if value == 'check':
            return value

    # Validate the task_planning_referee checkbox send True if is checked or false in not
    def validate_task_planning_referee(self, value):
        if value == 'check':
            return value

    '''

# Validator for previzion budget
class PrevisionCostValidator(serializers.ModelSerializer):
    class Meta:
        model = PrevisionCost
        fields = ['titled', 'amount','type']



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



class PrevisionCostSerializer(serializers.Serializer):
    # amount = serializers.DecimalField()
    # titled = serializers.DecimalField()


    def dictionary_with_prevision_cost(self):
        prevision_costs = PrevisionCost.objects.filter(type__type='CAR')
        titled = prevision_costs.titled
        amount = prevision_costs.amount
        bienveillance_prev = {
            "slug": "recap_recettes",
            "titre": "",
            "colonnes": [
                {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés
                {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants
            ],
            "lignes": [titled,amount],
            "total":True
        }
        return


