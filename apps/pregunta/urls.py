from django.urls import path

from apps.pregunta.views import list, delete, nuevo, edit


urlpatterns = [
    path('', list, name='list'),
    path('nuevo', nuevo, name='nuevo'),
    path('editar/<id_pregunta>', edit, name='edit'),
    path('eliminar/<id_pregunta>/', delete, name='eliminar'),
]