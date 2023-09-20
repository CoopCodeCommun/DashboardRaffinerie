from django.urls import path
from .views import dashboard, qonto, odoo, user, transaction_scroll

urlpatterns = [
    path('dashboard/', dashboard, name='tiqo_dashboard'),
    path('qonto/', qonto, name='qonto'),
    path('transaction_scroll/', transaction_scroll, name='transaction_scroll'),
    path('odoo/', odoo, name='odoo'),
    path('user/', user, name='user'),
]
