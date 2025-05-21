from django.contrib.auth.views import LoginView
from .forms import LoginForm, UsuarioCreateForm, UsuarioUpdateForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from autenticacion.models import Usuario

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

@login_required
def landing_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('usuario_list')
    else:
        form = UsuarioCreateForm()

    return render(request, 'crear_usuario.html', {
        'form': form,
        'titulo': 'Crear Usuario',
        'boton_texto': 'Guardar Usuario',
        'breadcrumb_items': [('Usuarios', '/usuarios/'), ('Crear', '')],
    })

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuario_list')
    else:
        form = UsuarioUpdateForm(instance=usuario)

    return render(request, 'editar_usuario.html', {
        'form': form,
        'titulo': 'Editar Usuario',
        'boton_texto': 'Actualizar Usuario',
        'breadcrumb_items': [('Usuarios', '/usuarios/'), ('Editar', '')],
    })


@login_required
def usuario_list(request):
    query = request.GET.get('q', '')
    usuarios = Usuario.objects.all()

    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(empresa__nombre__icontains=query) |
            Q(email__icontains=query)
        )

    paginator = Paginator(usuarios, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'usuarios': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'breadcrumb_items': [('Usuarios', None)],
    }
    return render(request, 'usuario_list.html', context)
