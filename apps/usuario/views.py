from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required

from apps.usuario.models import Usuario
from apps.usuario.forms import UsuarioForm, FormularioLogin


# Create your views here.

def list(request):
    admin = Usuario.objects.all().order_by('id')
    query = request.GET.get("buscar")
    if query:
        admin = Usuario.objects.annotate(full_name=Concat('nombres', Value(' '), 'apellido_paterno', Value(' '), 'apellido_materno'))\
            .filter(
            Q(full_name__icontains=query)|
            Q(dni__icontains=query)
            )
    paginator = Paginator(admin, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {'page_obj': page_obj, 'page': page_number}
    return render(request, 'usuario/list.html', contexto)


def nuevo(request):
    mensaje = ''
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid:
            count = Usuario.objects.filter(dni=request.POST['dni']).count()
            if count == 0:
                usuario = form.save()
                password = make_password(usuario.apellido_paterno + str(usuario.dni))
                user = User(
                    username = usuario.dni,
                    first_name = usuario.nombres,
                    password=password
                )
                group = Group.objects.get(name='Admin')
                user.save()
                group.user_set.add(user)
                usuario.user = User.objects.get(password__exact=user.password)
                usuario.save()
                return redirect('list')
            else:
                mensaje = 'Ya existe un usuario con ese número de DNI'
    else:
        form = UsuarioForm()
    return render(request, 'usuario/form.html', {'form':form, 'msg': mensaje})




class Login(FormView):
    template_name = 'usuario/login.html'
    form_class = FormularioLogin

    #if reques.user
    success_url = reverse_lazy('bienvenida')


    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)

    def form_valid(self,form):
        user = form.get_user()
        grupo = Group.objects.get(name='Admin')
        login(self.request, form.get_user())
        return super(Login,self).form_valid(form)            

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('accounts/login/')



@login_required
def bienvenida(request):
    userId = request.user.id
    usuario = User.objects.get(id = userId)
    context = {'usuario': usuario}
    return render(request, 'usuario/bienvenida.html', context)
