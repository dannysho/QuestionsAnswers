from django.urls import path

from apps.usuario.views import list, nuevo, Login, logoutUsuario, bienvenida 

urlpatterns = [
    path('', list, name='list'),
    path('nuevo', nuevo, name='nuevo'),
    path('accounts/login/', Login.as_view(), name="login"),
    path('logout', logoutUsuario, name='logout'),
    path('bienvenida', bienvenida, name='bienvenida'),
]