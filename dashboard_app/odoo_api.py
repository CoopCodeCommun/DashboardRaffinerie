import json, os, decimal

from django.contrib.sites import requests
import requests
from django.utils.text import slugify

# from tiqo_parser.models import Configuration, Label, AccountJournal, AccountAnalyticGroup, AccountAnalyticAccount, \
#     OdooContact, OdooArticles, Transaction, AccountAccount
# from tiqo_parser.serializers import LabelsSerializer

import logging

from dashboard_app.models import Contact, Configuration
from dashboard_app.utils import DecimalEncoder

logger = logging.getLogger(__name__)


class OdooApi():
    def __init__(self):
        config = Configuration.get_solo()
        self.login = config.odoo_login
        self.api_key = config.get_odoo_apikey()
        self.url = config.odoo_url
        self.odoo_dbname = config.odoo_dbname
        # if not any([self.login, self.api_key, self.url, self.odoo_dbname]):
        #     raise Exception("Bad Odoo credentials. Set its in the admin panel.")

        self.params: dict = {
            "db": f"{self.odoo_dbname}",
            "login": f"{self.login}",
            "apikey": f"{self.api_key}",
        }

    def test_config(self):
        url = f"{self.url}tibillet-api/xmlrpc/login"

        headers = {
            'content-type': 'application/json'
        }

        postdata = {}
        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()

        if response.status_code == 200:
            resp_json = response.json()
            status = resp_json.get('result').get('authentification')
            if status == True:
                return status
            else:
                logging.error(f"Odoo server OFFLINE or BAD KEY : {resp_json}")
                return resp_json.get('result').get('error')

        return response


    def get_all_contacts(self):
        # Cherche tous les contacts de Odoo et les renseigne dans la DB
        url = f"{self.url}tibillet-api/xmlrpc/search_read"
        headers = {
            'content-type': 'application/json'
        }

        postdata = {}
        postdata["search_read_data"] = {
            "model": "res.partner",
            "filters": [],
            "fields": ["name", "email", "id"],
        }

        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()
        if response.status_code == 200:
            resp_json = response.json()
            for contact in resp_json.get('result'):
                odoo_contact = Contact.objects.filter(id_odoo=contact.get('id'))
                if odoo_contact.exists():
                    print(f"Contact {contact.get('name')} already exists in DB. Updating it.")
                    odoo_contact.update(
                        name=contact.get('name'),
                        email=contact.get('email'),
                    )
                else:
                    print(f"Contact {contact.get('name')} doesn't exist in DB. Creating it.")
                    Contact.objects.create(
                        name=contact.get('name'),
                        email=contact.get('email'),
                        id_odoo=contact.get('id'),
                    )

        return Contact.objects.all()

    def gc_contact(self, email: str, name: str):
        url = f"{self.url}tibillet-api/xmlrpc/gc_contact"
        headers = {
            'content-type': 'application/json'
        }

        if not email:
            raise Exception("Email is required to create a contact in Odoo.")

        # On ajoute les infos de membre au post DATA
        postdata = {}
        postdata["membre"] = {
            "name": f"{name.capitalize()}",
            "email": f"{email}"
        }

        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()
        return response.json()


    """
    def get_all_articles(self):
        # Cherche tous les articles de Odoo et les renseigne dans la DB
        url = f"{self.url}tibillet-api/xmlrpc/search_read"
        headers = {
            'content-type': 'application/json'
        }

        postdata = {}
        postdata["search_read_data"] = {
            "model": "product.product",
            "filters": [],
            "fields": ["name", "id"],
        }

        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json:
                for article in resp_json.get('result'):
                    odoo_article = OdooArticles.objects.filter(id_odoo=article.get('id'))
                    if not odoo_article.exists():
                        odoo_article = OdooArticles.objects.create(
                            id_odoo=article.get('id'),
                            name=article.get('name'),
                        )
                        odoo_article.save()

        return OdooArticles.objects.all()

    def create_draft_invoice(self, transaction: Transaction):
        article: OdooArticles = transaction.odoo_article()
        compte_analytique: AccountAnalyticAccount = transaction.odoo_analytic_account()
        account_account: AccountAccount = transaction.account_account_id()
        account_journal: AccountJournal = transaction.odoo_journal_account()
        beneficiary = transaction.beneficiary.odoo_contact
        initiator = transaction.initiator.odoo_contact
        attachments = transaction.attachments.all()

        list_attachments = None
        if attachments.count() > 0:
            list_attachments = [(attachment.name, attachment.url_qonto) for attachment in attachments]


        # On ajoute les infos de membre au post DATA
        postdata = {}
        postdata["invoice_data"] = {
            'article': article.id_odoo,
            'compte_analytique': compte_analytique,
            'account_account': account_account,
            'account_journal': account_journal,
            'beneficiaire_id': beneficiary.id_odoo,
            'initiator_id': initiator.id_odoo,
            'invoice_name': transaction.label,
            'ammount_cents': transaction.amount_cents,
            'vat_amount': transaction.vat_amount,
            'date': transaction.emitted_at.date().strftime("%Y-%m-%d"),
            'attachments': list_attachments,
        }

        url = f"{self.url}tibillet-api/xmlrpc/tiqo_create_draft_invoice"
        headers = { 'content-type': 'application/json' }
        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()
        if response.status_code == 200:
            resp_json = response.json()
            print(resp_json)
            if resp_json.get('result'):
                invoice_draft_id = resp_json.get('result').get('invoice_draft_id')
                if invoice_draft_id :
                    transaction.odoo_invoice_id = invoice_draft_id
                    transaction.odoo_sended = True
                    transaction.save()
                    return resp_json

        return response

    def get_account_account(self):
        # Cherche tous les contacts de Odoo et les renseigne dans la DB
        url = f"{self.url}tibillet-api/xmlrpc/search_read"
        headers = {
            'content-type': 'application/json'
        }

        postdata = {}
        postdata["search_read_data"] = {
            "model": "account.account",
            "filters": [],
            "fields": ["name", "id", "code"],
        }

        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()
        if response.status_code == 200:
            resp_json = response.json()
            for account in resp_json.get('result'):
                account, created = AccountAccount.objects.get_or_create(
                    name=account['name'],
                    code=account['code'],
                    id_odoo=account['id'],

                )
            return AccountAccount.objects.all()

    def get_account_journal(self):
        url = f"{self.url}tibillet-api/xmlrpc/account_journal"

        headers = {
            'content-type': 'application/json'
        }

        postdata = {}
        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()

        if response.status_code == 200:
            resp_json = response.json()
            for name, id_odoo in resp_json.get('result').items():
                print(f'{str(name)} : {int(id_odoo)}')
                AccountJournal.objects.get_or_create(
                    name=name,
                    id_odoo=id_odoo,
                )
            return AccountJournal.objects.all()

        raise Exception(f"Odoo server OFFLINE or BAD KEY : {response}")

    def get_account_analytic(self):
        url = f"{self.url}tibillet-api/xmlrpc/account_analytic"

        headers = {
            'content-type': 'application/json'
        }

        postdata = {}
        postdata.update(self.params)
        data = json.dumps({
            "params": postdata,
        }, cls=DecimalEncoder)

        session = requests.session()
        response = session.post(url, data=data, headers=headers)
        session.close()

        if response.status_code == 200:
            resp_json = response.json()
            accounts = resp_json.get('result')
            for account in accounts:
                # On gère d'abord les groupes
                group = None
                if account.get('group_id'):
                    group, created = AccountAnalyticGroup.objects.get_or_create(
                        id_odoo=account.get('group_id')[0],
                        name=account.get('group_id')[1],
                    )

                # On gère ensuite les comptes analytiques
                account, created = AccountAnalyticAccount.objects.get_or_create(
                    id_odoo=account.get('id'),
                    name=account.get('name'),
                    code=account.get('code'),
                    group=group,
                )

            return AccountAnalyticAccount.objects.all()

        raise Exception(f"Odoo server OFFLINE or BAD KEY : {response}")
    """

