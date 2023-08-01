from django.shortcuts import render


def index(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'base.html', context=context)
