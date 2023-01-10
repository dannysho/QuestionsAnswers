from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.db.models import Q
from django.utils import timezone

from apps.pregunta.models import Pregunta, Respuesta
from apps.pregunta.forms import PreguntaForm, RespuestaForm
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
    pregunta = Pregunta.objects.get(id=id_pregunta)
    if request.method == 'POST':
        pregunta.delete()
        return redirect('list')
    return render(request, 'pregunta/delete.html', {'pregunta': pregunta})

def delete_respuesta(request, id_respuesta):
    respuesta = Respuesta.objects.get(id=id_respuesta)
    if request.method == 'POST':
        respuesta.delete()
        return redirect('list')
    return render(request, 'pregunta/delete_respuesta.html', {'respuesta': respuesta})


def nuevo(request):
    mensaje = ''
    if request.method == 'POST':
        form = PreguntaForm(request.POST, request.FILES)
        if form.is_valid():
            existe_pregunta = Pregunta.objects.filter(detalle_pregunta=request.POST['detalle_pregunta']).exists()
            if existe_pregunta:
                mensaje = 'Existe la pregunta'  
            else:
                pregunta = form.save(commit=False)
                pregunta.fecha = timezone.now()
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
            existe_correcta = Respuesta.objects.filter(Q(pregunta_id=id_pregunta) & Q(correcta=True)).count()
            if existe_correcta == 0:
                respuesta = form.save(commit=False)
                respuesta.pregunta_id = id_pregunta
                respuesta.fecha = timezone.now()
                respuesta.save()
            else:
                if request.POST['correcta'] == 'True':
                    print(request.POST['correcta'])
                    mensaje = 'Ya existe una respuesta correcta'
                else:
                    respuesta = form.save(commit=False)
                    respuesta.pregunta_id = id_pregunta
                    respuesta.fecha = timezone.now()
                    respuesta.save()
                    return redirect('/pregunta/list_respuesta/'+str(id_pregunta))
                        
    else:
        form = RespuestaForm()
    return render(request, 'pregunta/form_respuesta.html', {'form': form, 'msg': mensaje})


def list_respuesta(request, id_pregunta):
    respuesta = Respuesta.objects.filter(pregunta_id=id_pregunta).order_by('-fecha')
    query = request.GET.get("buscar")
    if query:
        respuesta = Respuesta.objects\
        .filter(Q(pregunta_id=id_pregunta) & Q(correcta__icontains=query))

    paginator = Paginator(respuesta, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {'page_obj': page_obj, 'page': page_number}
    return render(request, 'pregunta/list_respuesta.html', contexto)