# Create your views here.
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import TeacherSerializer
from users.models import Teacher
import jwt, datetime
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
class TeacherLoginView(APIView):
    def post(self, request):
        National_ID = request.data['National_ID']
        password = request.data['password']
        user = Teacher.objects.filter(National_ID=National_ID).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Wrong password!")

        payload = {
            'National_ID': user.National_ID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class TeacherView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        serializer = TeacherSerializer(user)

        return Response(serializer.data)

class TeacherLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You have been logged out.'
        }

        return response