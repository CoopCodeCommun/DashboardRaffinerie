from rest_framework import serializers

from dashboard_user.models import CustomUser
from .models import (AccountAccount, AccountAnalyticGroup, PrevisionCost, OrganizationalChart,
                     PrestationsVentsRecettesInt, RealCost, RealCostExternService, RealCostInternSpending)


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

# serializing data to adapt them to list methods or to validate them from update
class RealcostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = RealCost
        fields = ['user','username', 'date', 'proposition', 'validated', 'invoiced', 'payed', 'type', 'pk']

    def get_username(self, obj):
        return obj.user.username

    # Geting the checkbox values in false when it's not checked
    def to_internal_value(self, data):
        # Provide default values for unchecked checkboxes
        data.setdefault('validated', False)
        data.setdefault('invoiced', False)
        data.setdefault('payed', False)
        return super().to_internal_value(data)


# serialize RealCostExternService by adapting them to the list method or to validate their entry
class RealCostExternServiceSerializer(serializers.ModelSerializer):
    contact_name = serializers.SerializerMethodField()
    class Meta:
        model = RealCostExternService
        fields = ['contact','contact_name','titled', 'date', 'validated', 'payed','type','pk']

    def get_contact_name(self, obj):
        return obj.contact.name

    def to_internal_value(self, data):
        # Provide default values for unchecked checkboxes
        data.setdefault('validated', False)
        data.setdefault('payed', False)
        return super().to_internal_value(data)


# serialize RealCostInternSpending by adapting them to the list method or to validate their entry
class RealCostIntSpendSerializer(serializers.ModelSerializer):
    pole_name = serializers.SerializerMethodField()
    class Meta:
        model = RealCostInternSpending
        fields = ['pole','pole_name','date_cost','amount','type','pk']

    def get_pole_name(self,obj):
        return obj.pole.name


# serialize PrestationsVentsRecettesInt by adapting them to the list method or to validate their entry
class PrestationsVentsRecettesIntSerializer(serializers.ModelSerializer):
    groupe_name = serializers.SerializerMethodField()
    class Meta:
        model = PrestationsVentsRecettesInt
        fields = ['groupe_name', 'group','amount', 'recette', 'prev_ou_reel','pk']

    def get_groupe_name(self, obj):
        return obj.group.name


# serialize OrganizationalChart
class OrganizationalChartSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = OrganizationalChart
        fields = ['user','username','intern_services','settlement_agent','budget_referee','task_planning_referee', 'pk']

    def get_username(self, obj):
        return obj.user.username


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
