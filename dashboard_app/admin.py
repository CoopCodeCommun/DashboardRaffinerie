

from django.contrib import admin
from unfold.admin import ModelAdmin


from dashboard_app.models import (Contact, Badge, Configuration, AccountAnalyticGroup,
        Groupe, Pole, Project, Action, PrevisionCost, RealCost, RealCostExternService,
        RealCostInternSpending, PrestationsVentsRecettesInt, Grant)
from solo.admin import SingletonModelAdmin


# admin model for groupe:
@admin.register(Groupe)
class GroupeAdmin(ModelAdmin):
    # liste d'affichage dans l'interface admin
    list_display = ('name', 'code', 'visible')

    list_filter = ['code']

    # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

@admin.register(Pole)
class PoleAdmin(ModelAdmin):
    # liste d'affichage dans l'interface admin
    list_display = ('name', 'code', 'user', 'type', 'visible')

    list_filter = ('user', 'code')

    # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True



# create admin for project model
@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('name', 'code','pol_name', 'user', 'finished')
    # filter project by the fields ple and user
    list_filter = ('pole__name', 'user')


    # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def pol_name(self, obj):
        # assuring that the name of the foreign key will be showed
        return obj.pole.name if obj.pole else ''

    pol_name.short_description = 'Le nom du Pôle'



# create admin for Action model
@admin.register(Action)
class ActionAdmin(ModelAdmin):
    # the fields of action admin
    list_display = ('name', 'code', 'user', 'finished', 'project')

    list_filter = ('code', 'project__name', 'user')

     # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True



# admin for Previsional Cost
@admin.register(PrevisionCost)
class PrevisionCostAdmin(ModelAdmin):
    # list of fields
    list_display = ('titled','amount','type')

    # filtering based on the type of the Spendings
    list_filter = ['type__type']

    # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True



# Creating an admin for the real costs of bienveillance or intern service (prestation)
@admin.register(RealCost)
class RealCostAdmin(ModelAdmin):
    #creating the list of fields
    list_display = ('type_depense', 'user', 'date', 'proposition', 'validated', 'invoiced', 'paid')

    #filtering by type or user
    list_filter = ('type__type', 'user')

    # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


    def type_depense(self, obj):
        return obj.type.type if obj.type else ''

    type_depense.short_description = 'Dépenses réeles'



# admin class extern presta puchases
@admin.register(RealCostExternService)
class RealCostExternServiceAdmin(ModelAdmin):
    #list of fields
    list_display = ('titled', 'type_depense', 'contact', 'date', 'validated', 'payed')
    #filter
    list_filter = ('contact', 'type__type')

    def type_depense(self, obj):
        return obj.type.type if obj.type else ''

    type_depense.short_description = 'Dépenses réeles'
    # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


# admin for admin interne service
@admin.register(RealCostInternSpending)
class RealCostInternSpendingAdmin(ModelAdmin):
    #fields
    list_display = ('pole_name', 'type_depense', 'amount', 'date_cost')

    # filter by pole or type field
    list_filter = ('pole__name', 'type__type')

    # for the pole name as foreign key
    def pole_name(self, obj):
        return obj.pole.name if obj.type else ''

    pole_name.short_description = 'Nom du pole'

    def type_depense(self, obj):
        return obj.type.type if obj.type else ''

    type_depense.short_description = 'Dépenses réeles'

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


# creating admin for Recettes
@admin.register(PrestationsVentsRecettesInt)
class PrestationsVentsRecettesIntAdmin(ModelAdmin):
    # list of fields
    list_display = ('prev_ou_reel', 'group_name', 'recette_type', 'date', 'montant')

    # filter by type of recette if it's real or prevision and from the groupe name
    list_filter = ['prev_ou_reel', 'recette__type']
    #list_filter = ('prev_ou_reel', 'group__name', 'recette__type')

    def group_name(self, obj):
        return obj.group.name if obj.group else ''

    group_name.short_description = 'groupe'

    def recette_type(self, obj):
        return obj.recette.type if obj.recette else ''

    recette_type.short_description = 'Categorie de recette'



    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True



# admin for Grant model (subventions)
@admin.register(Grant)
class GrantAdmin(ModelAdmin):
    # fields of grant model
    list_display = ('label', 'referee', 'amount',
                    'account_date_automatic', 'account_date',
                    'partnaire', 'reference', 'request_date',
                    'acceptation_date', 'notification_date','global_budget',
                    'rested_spending', 'recived_amount'
                    )

    # Type de permissions pour l'admin
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    pass

@admin.register(Badge)
class BadgeAdmin(ModelAdmin):
    pass

@admin.register(AccountAnalyticGroup)
class AccountAnalyticGroupAdmin(ModelAdmin):
    pass

@admin.register(Configuration)
class ConfigurationAdmin(ModelAdmin, SingletonModelAdmin):
    pass

