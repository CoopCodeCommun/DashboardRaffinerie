# Generated by Django 4.2.4 on 2024-03-06 07:47

from django.db import migrations, models
import stdimage.models
import stdimage.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAccount',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('id_odoo', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AccountAnalyticAccount',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('id_odoo', models.SmallIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AccountAnalyticGroup',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('id_odoo', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AccountJournal',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('id_odoo', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('code', models.SmallIntegerField(verbose_name='Code')),
                ('finished', models.BooleanField(default=False, verbose_name='Terminé')),
            ],
            options={
                'verbose_name_plural': 'Actions',
            },
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('iban', models.CharField(max_length=150, unique=True, verbose_name='Iban')),
                ('bic', models.CharField(blank=True, max_length=10, null=True, verbose_name='Bic ou Swift')),
                ('currency', models.CharField(default='euro', max_length=15, verbose_name='Devise')),
                ('account_number', models.CharField(max_length=150, unique=True, verbose_name='Numéro de compte')),
            ],
            options={
                'verbose_name': 'Compte Bancaire',
                'verbose_name_plural': 'Comptes Bancaires',
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qonto_login', models.CharField(max_length=100)),
                ('qonto_apikey', models.CharField(max_length=200)),
                ('odoo_url', models.URLField()),
                ('odoo_login', models.CharField(max_length=100)),
                ('odoo_apikey', models.CharField(max_length=200)),
                ('odoo_dbname', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('id_odoo', models.SmallIntegerField()),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(choices=[('M', 'membership'), ('B', 'beneficiarie')], default='B', max_length=1)),
                ('nom', models.CharField(blank=True, max_length=100, null=True)),
                ('structure', models.CharField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('tel', models.CharField(blank=True, max_length=100, null=True)),
                ('adresse', models.CharField(blank=True, max_length=100, null=True)),
                ('image', stdimage.models.JPEGField(blank=True, force_min_size=False, null=True, upload_to='images/', validators=[stdimage.validators.MinSizeValidator(960, 540)], variations={'med': (960, 540), 'thumb': (270, 270, True)}, verbose_name='Image du contact')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(choices=[('CAR', 'bienveillance'), ('IN_S', 'prestation interne'), ('EX_S', 'Prestation externe'), ('SP_I', 'Dépense interne'), ('SUB', 'Subvention'), ('SER', 'Prestation'), ('S', 'Vente'), ('IN_R', 'Récette interne')], default='CAR', max_length=4)),
            ],
            options={
                'verbose_name_plural': 'Dépenses',
            },
        ),
        migrations.CreateModel(
            name='DepensesBienveillance',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField(auto_now=True)),
                ('proposition', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valide', models.BooleanField(default=False)),
                ('facture', models.BooleanField(default=False)),
                ('paye', models.BooleanField(default=False)),
                ('commentaire', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('account_date_automatic', models.DateField(auto_now_add=True, verbose_name='Date comptable (automatique)')),
                ('label', models.CharField(max_length=150, verbose_name='Libéllé')),
                ('referee', models.CharField(max_length=70, verbose_name='Référent')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='amount')),
                ('account_date', models.DateField(verbose_name='Date comptable')),
                ('partnaire', models.CharField(max_length=60, verbose_name='Partenaire')),
                ('reference', models.CharField(max_length=60, verbose_name='Référence')),
                ('request_date', models.DateField(verbose_name='Date de la demande')),
                ('acceptation_date', models.DateField(verbose_name="Date d'accéptation")),
                ('notification_date', models.DateField(verbose_name='Date de notification')),
                ('initial_request_link', models.URLField(blank=True, null=True, verbose_name='Lien de demande initiale')),
                ('convention_link', models.URLField(blank=True, null=True, verbose_name='Lien convention')),
                ('global_budget', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Budget global project')),
                ('spended_amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Montant dépensé')),
                ('rested_spending', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Reste à dépenser')),
                ('recived_amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Montant reçu')),
            ],
            options={
                'verbose_name': 'Subvention',
                'verbose_name_plural': 'Subventions',
            },
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('code', models.SmallIntegerField(verbose_name='Code')),
                ('visible', models.BooleanField(default=True, verbose_name='Visible')),
            ],
            options={
                'verbose_name': 'Groupe',
                'verbose_name_plural': 'Groupes',
            },
        ),
        migrations.CreateModel(
            name='InternServiceCaring',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField()),
                ('proposition', models.CharField(default='0 €', max_length=15)),
                ('validated', models.BooleanField(default=False, verbose_name='Validé')),
                ('invoiced', models.BooleanField(default=False, verbose_name='Facturé')),
                ('payed', models.BooleanField(default=False, verbose_name='Payé')),
                ('type', models.CharField(choices=[('CAR', 'bienveillance'), ('IN_S', 'Préstation interne')], default='CAR', max_length=4)),
            ],
            options={
                'verbose_name': 'Bienveillance prestation interne',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('client_or_supplier', models.CharField(choices=[('C', 'Client'), ('S', 'Fournisseur')], default='S', max_length=1, verbose_name='Choix: Client \\ Fournisseur ')),
                ('numero_facture', models.CharField(max_length=12, verbose_name='Numéro de facture')),
                ('nom', models.CharField(max_length=45, verbose_name='Nom de Client où Fournisseur')),
                ('date_invoicing', models.DateField(verbose_name='Date de facturation')),
                ('deadline', models.DateField(verbose_name="Date d'échéance")),
                ('account_date', models.DateField(blank=True, null=True, verbose_name='Date comptable')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='amount')),
                ('validated', models.BooleanField(default=False, verbose_name='Validé')),
                ('payed', models.BooleanField(default=False, verbose_name='Payé')),
            ],
            options={
                'verbose_name': 'Facture',
                'verbose_name_plural': 'Factures',
            },
        ),
        migrations.CreateModel(
            name='OrganizationalChart',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('intern_services', models.BooleanField(default=False, verbose_name='presta interne')),
                ('settlement_agent', models.BooleanField(default=False, verbose_name='garant du cadre')),
                ('budget_referee', models.BooleanField(default=False, verbose_name='référent budget / subvention')),
                ('task_planning_referee', models.BooleanField(default=False, verbose_name='référent tâche planning')),
            ],
            options={
                'verbose_name': 'Organigrame',
            },
        ),
        migrations.CreateModel(
            name='Pole',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30, verbose_name='Nom du pôle')),
                ('code', models.SmallIntegerField(verbose_name='Code')),
                ('visible', models.BooleanField(default=True, verbose_name='Visible')),
                ('type', models.CharField(choices=[('G', 'Groupe'), ('P', 'Pôle'), ('A', 'Action')], default='P', max_length=3)),
            ],
            options={
                'verbose_name': 'Pôle',
                'verbose_name_plural': 'Pôles',
            },
        ),
        migrations.CreateModel(
            name='PrestationsVentsRecettesInt',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('prev_ou_reel', models.CharField(choices=[('P', 'Prévisionnel'), ('R', 'Réel')], default='P', max_length=1, verbose_name='Prévisionnel ou Réel')),
                ('date', models.DateField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='amount')),
            ],
            options={
                'verbose_name_plural': 'Prestations Vents Recettes Internes',
            },
        ),
        migrations.CreateModel(
            name='PrevisionCost',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='amount')),
                ('titled', models.CharField(max_length=60, verbose_name='intitulé')),
            ],
            options={
                'verbose_name': 'Dépenses Prévisionnel',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('code', models.SmallIntegerField(verbose_name='Code')),
                ('finished', models.BooleanField(default=False, verbose_name='Terminé')),
            ],
            options={
                'verbose_name': 'Projet',
                'verbose_name_plural': 'Projets',
            },
        ),
        migrations.CreateModel(
            name='RealCost',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField(auto_now=True)),
                ('validated', models.BooleanField(default=False, verbose_name='validé')),
                ('invoiced', models.BooleanField(default=False, verbose_name='facturé')),
                ('payed', models.BooleanField(default=False, verbose_name='payé')),
                ('proposition', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='proposition')),
            ],
            options={
                'verbose_name': 'Bienvillance où Préstation interne',
                'verbose_name_plural': 'Bienvillances où Préstation internes',
            },
        ),
        migrations.CreateModel(
            name='RealCostExternService',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('titled', models.CharField(max_length=60, verbose_name='intitulé')),
                ('date', models.DateField(auto_now=True)),
                ('validated', models.BooleanField(default=False, verbose_name='Validé')),
                ('payed', models.BooleanField(default=False, verbose_name='Payé')),
            ],
            options={
                'verbose_name': 'Préstation externe / achat',
                'verbose_name_plural': 'Préstations externes / achats',
            },
        ),
        migrations.CreateModel(
            name='RealCostInternSpending',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='amount')),
                ('date_cost', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Dépense réele interne',
                'verbose_name_plural': 'Dépenses réeles internes',
            },
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(choices=[('P', 'Prestations'), ('SUB', 'Subventions / Appels à projet'), ('V', 'Ventes'), ('R_IN', 'Recettes internes')], default='P', max_length=4, verbose_name='Type de recette')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Rôle',
                'verbose_name_plural': 'Rôles',
            },
        ),
    ]