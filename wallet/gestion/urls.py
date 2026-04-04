from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name="pagina_inicio"),
    path('login',login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('accountlist/', CuentaListView.as_view(), name='account_list' ),
    path('create/', CuentaCreateView.as_view(), name='account_create'),
    path('edit/<int:pk>/', CuentaUpdateView.as_view(), name='account_update'),
    path('delete/<int:pk>/', CuentaDeleteView.as_view(), name='account_delete'),
    path('transfer/', TransaccionCreateView.as_view(), name='transaction_create')
]