from django.shortcuts import render


def index(request):
    name = 'glen'
    return render(request, 'base.html', {'name': name} )
