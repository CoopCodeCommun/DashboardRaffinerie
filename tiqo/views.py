from django.shortcuts import render


# Create your views here.


def index(request):
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'tiqo_index.html', context=context)
