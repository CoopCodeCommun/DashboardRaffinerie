from django.shortcuts import render


# Create your views here.


def index(request):
    context = {
        'user_email': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'tiqo_index.html', context=context)
