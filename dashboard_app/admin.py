from django.contrib import admin

from dashboard_app.models import Contact, Badge, Configuration, AccountAnalyticGroup
from solo.admin import SingletonModelAdmin
# Register your models here.


admin.site.register(Contact)
admin.site.register(Badge)
admin.site.register(Configuration, SingletonModelAdmin)
admin.site.register(AccountAnalyticGroup)
