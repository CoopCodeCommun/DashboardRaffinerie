import random

from django.db import models
from uuid import uuid4

from solo.models import SingletonModel
# Create your models here.
from stdimage import JPEGField
from stdimage.validators import MinSizeValidator

from dashboard_app.utils import fernet_encrypt, fernet_decrypt
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Badge(models.Model):
    # Des badges qui peuvent être attribués aux contacts
    # Many2Many car plusieurs contacts peuvent avoir le même badge
    # Et plusieurs badges peuvent avoir le même contact
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.name


### TABLES POUR DONNEE VENANT DE ODOO : ###

class Contact(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    id_odoo = models.SmallIntegerField()

    email = models.EmailField(max_length=100, null=True, blank=True)
    type = models.CharField(choices=(('M', 'membership'), ('B', 'beneficiarie')), max_length=1, default='B')

    nom = models.CharField(max_length=100, null=True, blank=True)
    structure = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)

    # Un lien vers la table Badge
    # Many2Many car plusieurs contacts peuvent avoir le même badge
    badge = models.ManyToManyField(Badge, related_name='contacts', blank=True)

    def badge_stringify(self):
        return ", ".join([str(badge) for badge in self.badge.all()])

    # Une image qui sera automatiquement convertie en JPG
    # avec la création de deux variations : 960x540 et un carré 270x270
    image = JPEGField(upload_to='images/',
                      validators=[MinSizeValidator(960, 540)],
                      variations={
                          'med': (960, 540),
                          'thumb': (270, 270, True)
                      },
                      delete_orphans=True,
                      verbose_name="Image du contact",
                      blank=True, null=True,
                      )

    # Une relation avec le modèle utilisateur.
    # Une fiche de contact peut être liée a un user
    user = models.ForeignKey('dashboard_user.CustomUser',
                             on_delete=models.PROTECT,
                             null=True, blank=True)

    def bienveillance_a_valider(self):
        return random.randint(0, 100)

    def bienveillance_a_facturer(self):
        return random.randint(0, 100)

    def bienveillance_a_payer(self):
        return random.randint(0, 100)

    def __str__(self):
        if self.nom:
            return self.nom
        elif self.structure:
            return self.structure
        elif self.email:
            return self.email
        return self.id_odoo


class AccountAccount(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, db_index=False)
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=100)
    id_odoo = models.SmallIntegerField()

    def __str__(self):
        return f"{self.code} {self.name}"


class AccountJournal(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, db_index=False)
    name = models.CharField(max_length=100, db_index=True)
    id_odoo = models.SmallIntegerField()

    def __str__(self):
        return self.name


class AccountAnalyticGroup(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, db_index=False)
    name = models.CharField(max_length=100, db_index=True)
    id_odoo = models.SmallIntegerField()

    def __str__(self):
        return self.name


class AccountAnalyticAccount(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, db_index=False)
    id_odoo = models.SmallIntegerField()
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=100)
    group = models.ForeignKey(AccountAnalyticGroup, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.group:
            return f"{self.group.name} > {self.name}"
        return self.name


### DONNEE DE CONFIGURATION ###

class Configuration(SingletonModel):
    # Table de configuration.
    # SigletonModel veut dire qu'il ne peut y avoir qu'une seule ligne (un seul enregistrement)
    # Autrement dit : pas besoin d'avoir plusieurs Odoo et Qonto.
    qonto_login = models.CharField(max_length=100)
    qonto_apikey = models.CharField(max_length=200)

    odoo_url = models.URLField()
    odoo_login = models.CharField(max_length=100)
    odoo_apikey = models.CharField(max_length=200)
    odoo_dbname = models.CharField(max_length=100)

    # Les clés sont stockées chiffrées sur la base de donnée
    # Pour renseigner ces champs, il faut passer par le shell Django
    # les deux fonctions servent à réaliser le chiffrement
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_qonto_apikey = self.qonto_apikey
        self.__original_odoo_apikey = self.odoo_apikey

    def save(self, *args, **kwargs):
        if self.__original_qonto_apikey != self.qonto_apikey:
            self.qonto_apikey = fernet_encrypt(self.qonto_apikey)

        if self.__original_odoo_apikey != self.odoo_apikey:
            self.odoo_apikey = fernet_encrypt(self.odoo_apikey)

        super().save(*args, **kwargs)

    def get_qonto_apikey(self):
        return fernet_decrypt(self.qonto_apikey)

    def get_odoo_apikey(self):
        return fernet_decrypt(self.odoo_apikey)


# Creating the groupe of poles
class Group(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=30, verbose_name="Nom du groupe")
    # The first number of the analytic code
    first_numbers_analytic_code = models.SmallIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(9)],
        default=1,
        verbose_name='Premiér nombre du code analytique')
    user = models.ForeignKey(settings.CONTACT_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="group",
                             null=True,
                             verbose_name="Members"
                             )
    class Meta:
        verbose_name = _("Groupe")
        verbose_name_plural = _("Groupes")


# Seting the pol with its analytic code
class Pole(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=30, verbose_name="Nom du pôle")
    # The second numbers of the analytic code
    second_numbers_analytic_code = models.SmallIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(9)],
        default=1,
        verbose_name='Deuxièm nombre du code analytique')
    group = models.ForeignKey(Group, related_name="pole", on_delete=models.PROTECT, verbose_name="Groupe")
    user = models.ForeignKey(settings.CONTACT_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="pole",
                             null=True,
                             verbose_name="Membre"
                             )
    class Meta:
        verbose_name = _("Pôle")
        verbose_name_plural = _("Pôles")


# Creating the project models of  groups and poles
class Project(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=30, verbose_name="Nom du projet")
    third_num_analytic_code = models.SmallIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(9)],
        default=1,
        verbose_name='Troisièm nombre du code analytique')
    pole = models.ForeignKey(Pole, related_name="project", on_delete=models.PROTECT, verbose_name="Pôle")
    user = models.ForeignKey(settings.CONTACT_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="project",
                             null=True,
                             verbose_name="Membre"
                             )
    class Meta:
        verbose_name = _("Projet")
        verbose_name_plural = _("Projets")


# Creating the action models of  groups and poles
class Action(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=30, verbose_name="Nom du projet")
    third_num_analytic_code = models.SmallIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(9)],
        default=1,
        verbose_name='Troisièm nombre du code analytique')
    project = models.ForeignKey(Project, related_name="action", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.CONTACT_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="action",
                             null=True,
                             verbose_name="Membre"
                             )
    class Meta:
        verbose_name_plural = ("Actions")


# Creating Organigrame model
class Organigrame(models.Model):
    pass

class BankAccount(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, db_index=False)
    iban = models.CharField(max_length=150, unique=True, verbose_name='Iban')
    bic = models.CharField(max_length=10, blank=True, null=True, verbose_name="Bic ou Swift")
    currency = models.CharField(max_length=15, default="euro", verbose_name='Devise')
    account_number = models.CharField(max_length=150, unique=True, verbose_name="Le numéro de compte")
    user = models.ForeignKey(
        settings.CONTACT_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="bank_account",
        verbose_name='Compte bancaire')


### TABLEAU SUIVI BUDGETAIRE DETAILLE ###

class DepensesBienveillance(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, db_index=False)

    date = models.DateField(auto_now=True)
    proposition = models.DecimalField(max_digits=10, decimal_places=2)
    valide = models.BooleanField(default=False)
    facture = models.BooleanField(default=False)
    paye = models.BooleanField(default=False)

    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    account_analytic_group = models.ForeignKey(AccountAnalyticGroup, on_delete=models.PROTECT)

    commentaire = models.TextField(blank=True, null=True)

