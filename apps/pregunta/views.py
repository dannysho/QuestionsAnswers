import json
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.utils import timezone

from apps.pregunta.models import Pregunta, Respuesta
from apps.usuario.models import Usuario
from apps.pregunta.forms import PreguntaForm, RespuestaForm
from apps.utils.ServiceResponse import ServiceResponse

# Create your views here.


def list(request):
    pregunta = Pregunta.objects.all().order_by('-fecha')
    query = request.GET.get("buscar")
    if query:
        pregunta = Pregunta.objects\
        .filter(titulo__icontains=query)

    paginator = Paginator(pregunta, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {'page_obj': page_obj, 'page': page_number}
    return render(request, 'pregunta/list.html', contexto)

def delete(request, id_pregunta):
    mensaje = ''
    userId = request.user.id
    usuario = Usuario.objects.filter(user_id = userId).exists()
    pregunta = Pregunta.objects.get(id=id_pregunta)
    if usuario:
        usu = Usuario.objects.get(user_id = userId)
        if pregunta.usuario_id == usu.id:
            if request.method == 'POST':
                pregunta.delete()
                return redirect('list')
        else:
            mensaje='No es el creador de la pregunta'
    else:
        mensaje='Debe loguearse para poder eliminar una pregunta'
    return render(request, 'pregunta/delete.html', {'pregunta': pregunta, 'msg': mensaje})

def delete_respuesta(request, id_respuesta):
    mensaje = ''
    userId = request.user.id
    usuario = Usuario.objects.filter(user_id = userId).exists()
    respuesta = Respuesta.objects.get(id=id_respuesta)
    if usuario:
        usu = Usuario.objects.get(user_id = userId)
        if respuesta.pregunta.usuario_id == usu.id:
            if request.method == 'POST':
                respuesta.delete()
                return redirect('list')
        else:
            mensaje = 'No es el creador de la pregunta'
    return render(request, 'pregunta/delete_respuesta.html', {'respuesta': respuesta, 'msg': mensaje})


def respuesta_correcta(request, id_respuesta):
    userId = request.user.id
    respuesta = Respuesta.objects.get(id__exact=id_respuesta)
    id_pregunta = respuesta.pregunta_id
    usu = Usuario.objects.get(user_id = userId)
    if respuesta.pregunta.usuario_id == usu.id:
        cont = Respuesta.objects.filter(Q(pregunta_id=id_pregunta) & Q(correcta=True)).count()
        if cont == 0:
            respuesta.correcta = True
            respuesta.save()
            response = ServiceResponse()
            response.addData('ok')
            data = json.dumps(response.getResult())
            return HttpResponse(data, content_type='application/json')
    


def nuevo(request):
    mensaje = ''
    userId = request.user.id
    usuario = Usuario.objects.filter(user_id = userId).exists()
    if request.method == 'POST':
        form = PreguntaForm(request.POST, request.FILES)
        if form.is_valid():
            existe_pregunta = Pregunta.objects.filter(detalle_pregunta=request.POST['detalle_pregunta']).exists()
            if existe_pregunta:
                mensaje = 'Existe la pregunta'  
            else:
                pregunta = form.save(commit=False)
                pregunta.fecha = timezone.now()
                if usuario:
                    usu = Usuario.objects.get(user_id = userId)
                    pregunta.usuario_id = usu.id
                pregunta.save()
                return redirect('list')
    else:
        form = PreguntaForm()
    return render(request, 'pregunta/form.html', {'form': form, 'msg': mensaje})


def edit(request, id_pregunta):
    mensaje = ''
    pregunta = Pregunta.objects.get(id=id_pregunta)
    if request.method == 'GET':
        form = PreguntaForm(instance=pregunta)
    else :
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            count = Pregunta.objects.filter(Q(detalle_pregunta=request.POST['detalle_pregunta']) & ~Q(id = pregunta.id)).count()
            if count == 0: 
                form.save()
                return redirect('list')
            else:
                mensaje = 'Ya existe la pregunta'
    return render(request, 'pregunta/form.html', {'form':form, 'msg': mensaje })



def nueva_respuesta(request, id_pregunta):
    mensaje = ''
    if request.method == 'POST':
        form = RespuestaForm(request.POST, request.FILES)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.pregunta_id = id_pregunta
            respuesta.fecha = timezone.now()
            respuesta.save()
            return redirect('/pregunta/list_respuesta/'+str(id_pregunta))
                        
    else:
        form = RespuestaForm()
    return render(request, 'pregunta/form_respuesta.html', {'form': form, 'msg': mensaje})


def list_respuesta(request, id_pregunta):
    respuesta = Respuesta.objects.filter(pregunta_id=id_pregunta).order_by('-correcta')
    query = request.GET.get("buscar")
    if query:
        respuesta = Respuesta.objects\
        .filter(Q(pregunta_id=id_pregunta) & Q(correcta__icontains=query))

    paginator = Paginator(respuesta, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {'page_obj': page_obj, 'page': page_number}
    return render(request, 'pregunta/list_respuesta.html', contexto)