from dataclasses import dataclass

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_htmx.middleware import HtmxDetails
from django.core.paginator import Paginator
from faker import Faker


# Create your views here.
# Typing pattern recommended by django-stubs:
# https://github.com/typeddjango/django-stubs#how-can-i-create-a-httprequest-thats-guaranteed-to-have-an-authenticated-user
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def dashboard(request):
    context = {
        'base_template': "_partial.html" if request.htmx else "_base.html",
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'tiqo_dashboard.html', context=context)


@dataclass
class Person:
    id: int
    name: str
    email: str


faker = Faker()
people = [Person(id=i, name=faker.name(), email=faker.email()) for i in range(1, 235)]


def qonto(request: HtmxHttpRequest) -> HttpResponse:
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=people, per_page=40).get_page(page_num)

    context = {
        'base_template': "_partial.html" if request.htmx else "_base.html",
        'user': request.user if request.user.is_authenticated else None,
        "page": page,
    }
    return render(request, 'tiqo_qonto.html', context=context)


def transaction_scroll(request: HtmxHttpRequest) -> HttpResponse:
    # time.sleep(1)
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=people, per_page=40).get_page(page_num)
    context = {
        "page": page,
    }
    return render(request, 'tiqo_transaction_scroll.html', context=context)

def odoo(request):
    context = {
        'base_template': "_partial.html" if request.htmx else "_base.html",
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'tiqo_odoo.html', context=context)


def user(request):
    context = {
        'base_template': "_partial.html" if request.htmx else "_base.html",
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'tiqo_user.html', context=context)
