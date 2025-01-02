import pickle

from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import jwt, datetime, os
from users.models import OnlineClass, Teacher, Classes, Student
# Create your views here.

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class TeacherEnterOnlineClass(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no teacher with this National_ID")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")


        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            return Response({"message":"There is no class with this information"})

        mylink = OnlineClass.objects.filter(Classes=myclass).first()
        if not mylink:
            creds = None
            # Load credentials from a saved token file
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # Authenticate if no valid credentials are found
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save credentials for future use
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            # Build the service
            service = build('calendar', 'v3', credentials=creds)

            # Event details
            event = {
                'summary': 'Google Meet Event',
                'description': 'Meeting via Google Meet',
                'start': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat(),
                    'timeZone': 'UTC',
                },
                'conferenceData': {
                    'createRequest': {
                        'requestId': 'sample123',  # Unique ID for the request
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                    },
                },
                'attendees': [
                    {'email': 'example1@gmail.com'},
                    {'email': 'example2@gmail.com'}
                ],
            }

            # Create the event
            created_event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()

            # Output the Meet link
            print('Google Meet Link:', created_event['conferenceData']['entryPoints'][0]['uri'])
            myvar = created_event['conferenceData']['entryPoints'][0]['uri']
            mylink = OnlineClass.objects.create(Classes=myclass, link=created_event['conferenceData']['entryPoints'][0]['uri'])
            mylink.save()
            try:
                os.remove('token.pickle')
            except:
                pass
            return Response({'message':f'{myvar}'})
        myvar = mylink.link
        return Response({'message': f'{myvar}'})

class StudentEnterOnlineClass(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no teacher with this National_ID")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")


        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            return Response({"message":"There is no class with this information"})

        mylink = OnlineClass.objects.filter(Classes=myclass).first()
        if not mylink:
            return Response({'message':'There is no meet for this class yet'})
        myvar = mylink.link
        return Response({'message': f'{myvar}'})