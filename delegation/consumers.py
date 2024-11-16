import json
from channels.generic.websocket import AsyncWebsocketConsumer
from delegation.models import messages
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
#import asyncio

@database_sync_to_async
def message_db(message, user_id, chat_id):
    messages.objects.create(content=message, user_id=user_id, chat_id=chat_id)

@database_sync_to_async
def get_messages(user_id, chat_id):
    all_messages = messages.objects.filter(chat_id=chat_id)
    list_messages = []
    # full_name = f'{user_object.first_name} {user_object.last_name}'
    for i in all_messages:
        if user_id == i.user_id:
            list_messages.append([i.id, i.content, str(i.date_create).split('.')[0], 'current'])
        else:
            user_object = User.objects.get(id=i.user_id)
            full_name = f'{user_object.first_name} {user_object.last_name}'
            # print(full_name)
            list_messages.append([i.id, i.content, str(i.date_create).split('.')[0], i.user_id, full_name])
    return list_messages


class MessenerConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        user = self.scope["user"]
        self.user_id = user.id
        print(self.user_id)
        if self.user_id != None:
            print('connected_web')
            await self.accept()  # Принять соединение


    async def disconnect(self, close_code):
        pass  # Обработка отключения

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #print(text_data_json['type'])
        if text_data_json['type'] == 'send_message':
            message = text_data_json['message']
            chat_id = text_data_json['chat_id']

            await message_db(message, self.user_id, chat_id)
            await self.send(text_data=json.dumps({
                'message': message
            }))
        elif text_data_json['type'] == 'get_messages':
            chat_id = text_data_json['chat_id']
            all_messages = await get_messages(self.user_id, chat_id)
            info = {
                'all_messages': all_messages
            }
            # print(info)
            await self.send(text_data=json.dumps(info))
