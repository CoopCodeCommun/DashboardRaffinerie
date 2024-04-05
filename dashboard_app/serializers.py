from rest_framework import serializers

from dashboard_user.models import CustomUser
from .models import (AccountAccount, AccountAnalyticGroup, PrevisionCost, OrganizationalChart,
                     PrestationsVentsRecettesInt, RealCost, RealCostExternService,
                     Transaction,RealCostInternSpending)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid',
            'email',
        ]
        read_only_fields = ('uuid', 'email',)


# # Validator for OrganizationalChart
# class OrganizationalChartValidator(serializers.ModelSerializer):
#     class Meta:
#         model = OrganizationalChart
#
#         fields = ['user', 'intern_services', 'settlement_agent', 'budget_referee', 'task_planning_referee']
#


# Validator for previzion budget
class PrevisionCostSerializer(serializers.ModelSerializer):
    #adding fields that aren't in the data of our model
    # like for exemple url1 and url2
    # url1 = serializers.SerializerMethodField()
    # url2 = serializers.SerializerMethodField()

    class Meta:
        model = PrevisionCost
        fields = ['titled', 'amount','type', 'pk']#, 'url1','url2']

    # def get_url1(self, obj):
    #     return 'suivi_budg'
    #
    # def get_url2(self, obj):
    #     return 'depenses_recettes'

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


    def to_internal_value(self, data):
        # Provide default values for unchecked checkboxes
        data.setdefault('intern_services', False)
        data.setdefault('settlement_agent', False)
        data.setdefault('budget_referee', False)
        data.setdefault('task_planning_referee', False)
        return super().to_internal_value(data)


class TransactionSerializer(serializers.ModelSerializer):
    code_analytique = serializers.SerializerMethodField()
    emitted_at = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['transaction_id',
                  'emitted_at',
                  'description',
                  'amount', 'iban',
                  'label_fournisseur',
                  'code_analytique',
                  'attachment_ids',
                  'api_uuid', 'pk']

    # Sending the date and the hour (cleanded data
    def get_emitted_at(self, obj):
        return obj.emitted_at.strftime('%Y-%m-%d %H:%M')

    # Method to send "donnée manquant" or the data note (description) if there is
    # not missed data
    def get_description(self,obj):
        return obj.note if obj.note else 'Donnée manquante'

    # sending the analytic code in fonction of the type of the data
    def get_code_analytique(self, obj):
        if obj.reference:
            if len(obj.reference) < 4:
                return obj.reference
            # Sending just the code analytique if it's start with a number else send the string
            # return obj.reference[:6] if obj.reference[0] in '123456789' else obj.reference
            return ''.join([x for x in obj.reference[:6] if x in '0123456789'])\
                if obj.reference[1] and obj.reference[2]  in '123456789' else obj.reference

        return 'Donnée manquante'



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
