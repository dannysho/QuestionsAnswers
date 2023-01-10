from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.db.models import Q
from django.utils import timezone

from apps.pregunta.models import Pregunta
from apps.pregunta.forms import PreguntaForm
# Create your views here.


def list(request):
    pregunta = Pregunta.objects.all().order_by('-fecha')
    query = request.GET.get("buscar")
    if query:
        pregunta = Pregunta.objects\
        .filter(curso__icontains=query)

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

