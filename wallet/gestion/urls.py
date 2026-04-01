from django.urls import path
from .views import home, login_view

urlpatterns = [
    path('',home, name="pagina_inicio"),
    path('login',login_view, name="login"),
]