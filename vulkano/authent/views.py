from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TwoFactorCode
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import PerfilUsuario

def bienvenida_view(request):
    return render(request, "bienvenida.html")

def administrar_usuarios_view(request):
    perfiles = PerfilUsuario.objects.select_related('user', 'sucursal').all()
    return render(request, "usuarios.html", {"perfiles": perfiles})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import PerfilUsuario, Sucursal
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import PerfilUsuario, Sucursal
from django.contrib.auth.models import User
from django.contrib import messages

def crear_usuario_view(request):
    sucursales = Sucursal.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        sucursal_id = request.POST.get("sucursal")
        rol = request.POST.get("rol")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            sucursal = Sucursal.objects.get(id=sucursal_id)
            PerfilUsuario.objects.create(user=user, sucursal=sucursal, rol=rol)
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('administrar_usuarios')

    return render(request, "crear_usuario.html", {
        "sucursales": sucursales
    })

from django.shortcuts import get_object_or_404

def editar_usuario_view(request, perfil_id):
    perfil = get_object_or_404(PerfilUsuario, id=perfil_id)
    sucursales = Sucursal.objects.all()

    if request.method == "POST":
        email = request.POST.get("email")
        sucursal_id = request.POST.get("sucursal")
        rol = request.POST.get("rol")
        activo = request.POST.get("activo") == "True"

        # Actualizar información
        perfil.user.email = email
        perfil.user.save()
        perfil.sucursal = Sucursal.objects.get(id=sucursal_id)
        perfil.rol = rol
        perfil.activo = activo
        perfil.save()

        messages.success(request, "Usuario actualizado exitosamente.")
        return redirect('administrar_usuarios')

    return render(request, "editar_usuario.html", {
        "perfil": perfil,
        "sucursales": sucursales,
    })


def administrar_usuarios_view(request):
    perfiles = PerfilUsuario.objects.select_related('user', 'sucursal').all()
    sucursales = Sucursal.objects.all()

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        sucursal_id = request.POST.get('sucursal')
        rol = request.POST.get('rol')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            sucursal = Sucursal.objects.get(id=sucursal_id)
            PerfilUsuario.objects.create(user=user, sucursal=sucursal, rol=rol)
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('administrar_usuarios')

    return render(request, "usuarios.html", {
        "perfiles": perfiles,
        "sucursales": sucursales,
    })


def registro_view(request):
    mensaje = ""
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            mensaje = "Las contraseñas no coinciden."
        elif User.objects.filter(username=username).exists():
            mensaje = "Este nombre de usuario ya existe."
        elif User.objects.filter(email=email).exists():
            mensaje = "Ya hay una cuenta con este correo."
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            return redirect("login_mfa")

    return render(request, "registro.html", {"mensaje": mensaje})

class LoginMFAView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, req):
        u, p = req.data.get('username'), req.data.get('password')
        user = authenticate(req, username=u, password=p)
        if not user:
            return Response({"detail":"Credenciales inválidas"}, status=401)
        code_rec = TwoFactorCode.create_for_user(user)
        send_mail('Tu código 2FA', f'Código: {code_rec.code}', 'joluro86@hotmail.com',[user.email],fail_silently=True)
        return Response({"detail":f"Código enviado {user.email}"}, status=200)

class VerifyMFAView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, req):
        u, code = req.data.get('username'), req.data.get('code')
        try: user = authenticate(req, username=u) or user_model.objects.get(username=u)
        except: return Response({"detail":"Usuario no encontrado"},404)
        rec = TwoFactorCode.objects.filter(user=user).latest('created_at')
        if not rec.is_valid() or rec.code!=code:
            return Response({"detail":"Código inválido o expirado"},400)
        refresh = RefreshToken.for_user(user)
        rec.delete()
        return Response({"access":str(refresh.access_token),"refresh":str(refresh)},200)

