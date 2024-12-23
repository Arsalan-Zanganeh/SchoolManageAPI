import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import Chat, Message,AccountForChat
from users.models import User, NotificationStudent
from users.models import Student, Teacher
import jwt
from auth.settings import SECRET_KEY

class ChatConsumer(WebsocketConsumer):
    connected_users = set()

    def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        try:
            self.chat = Chat.objects.get(id=self.chat_id)
        except Chat.DoesNotExist:
            self.close()
            return
            
        headers = dict(self.scope['headers'])
        auth_header = headers.get(b'authorization', b'').decode()
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            national_id = decoded.get("National_ID")
            user = None
            account_user = None
            student = Student.objects.filter(National_ID=national_id).first()
            if student:
                user = student
                account_user = AccountForChat.objects.get(student=student)
            teacher = Teacher.objects.filter(National_ID=national_id).first()
            if teacher:
                user = teacher
                account_user = AccountForChat.objects.get(teacher=teacher)
            user2 = User.objects.filter(National_ID=national_id).first()
            if user2:
                user = user2
                account_user = AccountForChat.objects.get(user=user2)

           # account_user = AccountForChat.objects.get(user=user,teacher=teacher,student=student)
           
           

            # if not account_user:
            #     account_user = AccountForChat.objects.get(student__National_ID=national_id)
            #     if not account_user:
            #         account_user = AccountForChat.objects.get(teacher__National_ID=national_id)
            #         user = account_user.teacher
            #     else:
            #         user = account_user.student
            # else:
            #     user = account_user.user

            


            if user:
                self.scope['user'] = user
                self.scope['account_user'] = account_user
                self.connected_users.add(user.National_ID)
            else:
                print("hello")
                return
        else:

            self.send_error_and_close('You are not authenticated')
            return
        
        
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        
        messages = self.get_chat_messages()
        self.send(text_data=json.dumps({
            'type': 'chat_history',
            'messages': messages
        }, cls=DjangoJSONEncoder))

    def get_chat_messages(self):
        return list(self.chat.messages.all().order_by('-timestamp').values(
            'content', 'sender__student__National_ID','sender__teacher__National_ID', 'timestamp'
        ))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        user = self.scope.get("user")
        if user:
            self.connected_users.remove(user.National_ID)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]
        account_user = self.scope["account_user"]


        if not user or user.National_ID not in self.connected_users:
            self.send_error_and_close('You are not authenticated')
            return
        
        db_message = Message.objects.create(
            chat=self.chat,
            content=message,
            sender=account_user
        )
        tmp = None
        if db_message.sender.user:
            tmp = db_message.sender.user.National_ID
        if db_message.sender.student:
            tmp = db_message.sender.student.National_ID
        if db_message.sender.teacher:
            tmp = db_message.sender.teacher.National_ID
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message", 
                "message": db_message.content, 
                "username": tmp,
                "timestamp": db_message.timestamp.isoformat(),
            }
        )
        
        # for member in self.chat.participants.exclude(user__National_ID__in=self.connected_users):
        #     NotificationStudent.objects.create(
        #         message=f"New message in {self.chat_id} from {tmp}",
        #         student=member,
        #         seen=False,
        #         archive=False
        #     )
            

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))
    
    def send_error_and_close(self, message):
        self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))
        self.close()
