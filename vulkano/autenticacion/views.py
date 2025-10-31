from django.contrib.auth.views import LoginView
from .forms import LoginForm, UsuarioCreateForm, UsuarioUpdateForm, generar_username_auto
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from autenticacion.models import Usuario
from django.http import JsonResponse
from producto.models import Producto


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

def landing_view(request):
    productos = Producto.objects.all()
    return render(request, "landing.html", {"productos": productos})


@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('usuario_list')
    else:
        # Inicializa campos vacíos y prellena el username si hay nombre y apellido
        initial = {}
        if 'first_name' in request.GET and 'last_name' in request.GET:
            initial['username'] = generar_username_auto(request.GET['first_name'], request.GET['last_name'])
        form = UsuarioCreateForm(initial=initial)

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

def generar_username_auto(nombre, apellidos):
    nombre_partes = nombre.strip().split()
    apellido_partes = apellidos.strip().split()

    nombre_base = nombre_partes[0].lower() if nombre_partes else ''
    primer_apellido = apellido_partes[0].lower() if apellido_partes else ''
    inicial_segundo_apellido = apellido_partes[1][0].lower() if len(apellido_partes) > 1 else ''

    base = f"{nombre_base[0]}{primer_apellido}{inicial_segundo_apellido}"

    Usuario = get_user_model()
    username = base

    i = 1
    while Usuario.objects.filter(username=username).exists():
        # Agrega más letras del primer nombre, luego del segundo nombre si hay
        if i < len(nombre_base):
            username = f"{nombre_base[:i+1]}{primer_apellido}{inicial_segundo_apellido}"
        elif len(nombre_partes) > 1 and i - len(nombre_base) < len(nombre_partes[1]):
            segunda_parte = nombre_partes[1]
            extra = segunda_parte[:i - len(nombre_base) + 1]
            username = f"{nombre_base}{extra}{primer_apellido}{inicial_segundo_apellido}"
        else:
            username = f"{base}x"
        i += 1

    return username

def validar_username(request):
    username = request.GET.get('username', '').strip()
    empresa_id = request.GET.get('empresa_id')

    if username and empresa_id:
        existe = Usuario.objects.filter(username=username, empresa_id=empresa_id).exists()
        return JsonResponse({'existe': existe})
    return JsonResponse({'existe': False})