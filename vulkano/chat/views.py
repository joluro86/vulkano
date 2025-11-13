from django.shortcuts import render
from .models import Room, Message
from django.contrib.auth.decorators import login_required

@login_required
def show_rooms(request):
    rooms=Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def join_room(request, room_slug):
    room = Room.objects.get(slug=room_slug)
    messages = Message.objects.filter(room=room)
    return render(request, 'room.html', {'room': room, 'messages': messages})