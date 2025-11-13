import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Message, Room

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = 'sala_chat_%s' % self.room_slug
        self.room = Room.objects.get(slug=self.room_slug)
        self.user = self.scope['user']

        print('Conexión establecida al room_group_name ' + self.room_group_name)
        print('Conexión establecida channel_name ' + self.channel_name)

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self):
        print('Se ha desconectado')
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        print('Mensaje recibido del WebSocket: ' + text_data)
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()
    
            if not message:
                print('Mensaje vacío, no se guarda ni envía')
                return

            print(f'Usuario: {self.user}, Mensaje: {message}, Sala: {self.room}')
            msg = Message.objects.create(
                room=self.room,
                user=self.user,
                message=message,
                timestamp=timezone.now()
            )

            print(f'Mensaje guardado en la base de datos: {msg}')

            # Broadcast al grupo
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': msg.message,
                    'username': msg.user.get_username(),
                    'datetime': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )

        except json.JSONDecodeError as e:
            print('Hubo un error al decodificar el JSON: ', e)
        except KeyError as e:
            print('Clave faltante en el JSON: ', e)
        except Exception as e:
            print('Error desconocido ##################################################################################################################################: ', e)

    def chat_message(self, event):
        print('Evento recibido para enviar mensaje: ', event)
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        print(f'Enviando mensaje al WebSocket: {message} de {username} a las {datetime}')

        self.send(text_data=json.dumps({
            'message':message,
            'username': username,
            'datetime': datetime
        }))