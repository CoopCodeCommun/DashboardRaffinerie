from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard_app.serializers import UserSerializer


# from rest_framework import routers, serializers, viewsets
# from rest_framework import viewsets,

def index(request):
    """
    Livre un template HTML
    Ne passe pas par l'api Django-Rest-Framework mais par le moteur de template de Django
    Template base.html dans le dossier templates
    avec un contexte qui contient le nom de l'utilisateur
    """
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'example.html', context=context)


def suivi_budgetaire(request):
    """
    Livre un template HTML suivi_budgetaire.html
    Extension du template base.html
    """
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'suivi_budgetaire.html', context=context)

### TEST API AVEC MODEL USER ###

@permission_classes([AllowAny])
class user_api(APIView):
    def get(self, request):
        """
        API REST qui n'utile pas de serializer
        """
        User = get_user_model()
        serializer = UserSerializer(User.objects.all(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class user_solo_api(APIView):
    def get(self, request, uuid=None):
        User = get_user_model()
        serializer = UserSerializer(User.objects.get(pk=uuid))

        return Response(serializer.data, status=status.HTTP_200_OK)



class user_viewset(viewsets.ViewSet):
    """
    API CRUD : create read update delete
    Exemple :
    GET /api/user/ : liste des utilisateurs
    GET /api/user/<uuid>/ : utilisateur avec primary key <uuid>
    """

    def list(self, request):
        User = get_user_model()
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        User = get_user_model()
        serializer = UserSerializer(User.objects.get(pk=pk))
        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


### FIN TEST API AVEC MODEL USER ###