from django.shortcuts import get_object_or_404, redirect, render
from .models import Room, Message
from django.contrib.auth.decorators import login_required
from autenticacion.decorators import group_required
from django.utils import timezone 
from django.contrib import messages as dj_messages

@login_required
def show_rooms(request):
    rooms=Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})


@group_required('Administrador', 'Operario')
def join_room(request, room_slug):

    room = Room.objects.get(slug=room_slug)
    if room.status != 'active':
            room.status = 'active'
            if room.started_at is None:
                room.started_at = timezone.now()
            room.save()

    messages = Message.objects.filter(room=room)
    return render(request, 'room.html', {'room': room, 'messages': messages})


@group_required('Administrador', 'Operario')
def cerrar_sala(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)

    if room.status != 'closed':
        room.status = 'closed'
        room.closed_at = timezone.now()
        room.save()
        dj_messages.success(request, f'La sala "{room.name}" ha sido cerrada.')
    else:
        dj_messages.info(request, f'La sala "{room.name}" ya estaba cerrada.')

    return redirect('room_list')


@login_required
def mi_sala_chat(request):
    
    user = request.user
    slug = f"cliente-{user.id}"
    room, created = Room.objects.get_or_create(
        slug=slug,
        defaults={
            'name': f"Chat de {user.get_full_name() or user.username}"
        }
    )

    if room.status == 'closed':
        room.status = 'pending'
        room.save()
    
    puede_cerrar = request.user.groups.filter(
        name__in=['Administrador', 'Operario']
    ).exists()

    messages = Message.objects.filter(room=room)

    return render(request, 'room.html', {'room': room, 'messages': messages, 'puede_cerrar': puede_cerrar})