from django.urls import path

from apps.pregunta.views import list, delete, nuevo, edit, list_respuesta, nueva_respuesta, delete_respuesta, respuesta_correcta


urlpatterns = [
    path('', list, name='list'),
    path('nuevo', nuevo, name='nuevo'),
    path('editar/<id_pregunta>', edit, name='edit'),
    path('eliminar/<id_pregunta>/', delete, name='eliminar'),
    path('eliminar_respuesta/<id_respuesta>/', delete_respuesta, name='eliminar_respuesta'),
    path('respuesta_correcta/<id_respuesta>/', respuesta_correcta, name='respuesta_correcta'),
    path('list_respuesta/<id_pregunta>', list_respuesta, name='list_respuesta'),
    path('nueva_respuesta/<id_pregunta>', nueva_respuesta, name='nueva_respuesta'),
]