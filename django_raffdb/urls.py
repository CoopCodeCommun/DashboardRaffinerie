"""
URL configuration for django_raffdb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers

from dashboard_app.views import user_viewset
from django.conf.urls.static import  static

router = routers.DefaultRouter()

# Exemple :
# curl http://localhost:8000/apiuser/
# curl http://localhost:8000/apiuser/fb021856-973c-4d17-810d-d0cc4c8f3f84/
router.register(r'apiuser', user_viewset, basename='user')



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include('rest_framework.urls')),
    path("", include('dashboard_app.urls')),
    path("tiqo/", include('tiqo.urls')),
    # path('', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += path('__reload__/', include("django_browser_reload.urls")),

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)