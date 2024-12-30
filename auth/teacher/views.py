# Create your views here.
import pytz
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import TeacherSerializer, ClassSerializer, StudentSerializer, AttendanceFormSerializer
from users.models import Teacher, ClassStudent, Classes, Student, StudentAttendance, SchoolTeachers, PrinicipalCalendar, \
    PrincipalAddEvent, School
import jwt, datetime, os
from django.contrib.auth.hashers import make_password, check_password
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar"]


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
        # response.set_cookie(key='jwt', value=token, httponly=True, samesite='None', secure=True)
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

class TeacherClassesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Teacher Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()

        classes = Classes.objects.filter(Teacher=teacher).all()
        if not classes:
            raise AuthenticationFailed("Class not found!")

        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)


class TeacherClassStudentsView(APIView):
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
            return Response({"message":"There is no class with this National_ID"})

        students1 = ClassStudent.objects.filter(Classes=myclass).values_list('Student__National_ID', flat=True)
        students2 = Student.objects.filter(National_ID__in=students1)
        serializer = StudentSerializer(students2, many=True)
        return Response(serializer.data)

class TeacherCheckStudentAttendance(APIView):
    def post(self, request):
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

        student = Student.objects.filter(National_ID=request.data['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no student with this National_ID")

        classStudent = ClassStudent.objects.filter(Classes=myclass, Student=student).first()
        if not classStudent:
            return Response({"message":"There is no class with this information"})

        myobj = StudentAttendance.objects.filter(ClassStudent=classStudent, Date=request.data['Date']).first()
        if not myobj:
            myobj2 = StudentAttendance.objects.create(ClassStudent=classStudent, Date=request.data['Date'], Absent=request.data['Absent'])
            myobj2.save()
        else:
            myobj.Absent = request.data['Absent']
            myobj.save()
        if request.data['Absent'] == True:
            return Response({"message":"Absent"})
        return Response({"message":"Present"})

class TeacherWatchAttendance(APIView):
    def post(self, request):
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

        classStudent = ClassStudent.objects.filter(Classes=myclass).first()
        if not classStudent:
            return Response({"message":"There is no class with this information"})

        myobj = StudentAttendance.objects.filter(ClassStudent=classStudent, Date=request.data['Date']).first()
        if not myobj:
            myvals = ClassStudent.objects.filter(Classes=myclass).values_list('Student__National_ID', flat=True)
            students = Student.objects.filter(National_ID__in=myvals).all()
            for student in students:
                myclassStudent = ClassStudent.objects.filter(Classes=myclass, Student=student).first()
                myobj2 = StudentAttendance.objects.create(ClassStudent=myclassStudent, Date=request.data['Date'])
                myobj2.save()
            mydata = StudentAttendance.objects.filter(ClassStudent__Classes=myclass, Date=request.data['Date']).all()
            serializer = AttendanceFormSerializer(mydata, many=True)
            return Response(serializer.data)
        mydata = StudentAttendance.objects.filter(ClassStudent__Classes=myclass, Date=request.data['Date']).all()
        serializer = AttendanceFormSerializer(mydata, many=True)
        return Response(serializer.data)

class TeacherCalendarView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myschool = SchoolTeachers.objects.filter(Teacher__National_ID=payload['National_ID']).first()
        if not myschool:
            raise AuthenticationFailed("There is no teacher with this National_ID")
        school = myschool.School
        if not school:
            raise AuthenticationFailed("There is no such a school for this teacher")

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, "../media/profile_image/credentials.json")
        if not mymodel:
            # mymodel = PrinicipalCalendar.objects.create(School=school)
            # token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     credentials_path, SCOPES
            # )
            # creds = flow.run_local_server(port=0)
            # mymodel.is_valid=True
            # mymodel.save()
            # with open(token_path, "w") as token:
            #     token.write(creds.to_json())
            raise AuthenticationFailed("You can't access google calendar because there is no calendar created yet")
        elif not mymodel.is_valid:
            # token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     credentials_path, SCOPES
            # )
            # creds = flow.run_local_server(port=0)
            # mymodel.is_valid=True
            # mymodel.save()
            # with open(token_path, "w") as token:
            #     token.write(creds.to_json())
            raise AuthenticationFailed("You can't access google calendar because there is no calendar created yet")

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        try:
            # Initialize Google Calendar API service
            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])


            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
            calendar_list = service.calendarList().list().execute()
            primary_calendar = next((cal for cal in calendar_list['items'] if cal.get('primary')), None)
            calendar_id = None
            if primary_calendar:
                calendar_id =  primary_calendar['id']  # This is the calendar ID for the primary calendar
            else:
                raise AuthenticationFailed("Primary calendar not found.")
            calendar_url = f"https://calendar.google.com/calendar/u/0/r?cid="+str(calendar_id)
            webbrowser.open(calendar_url)
            return Response({"message":"It was done successfully"})

        except:
            return Response({"message":"An error occurred"})

class UserAddSchoolEvent(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        if not school:
            raise AuthenticationFailed("There is no such a school")

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, "../media/profile_image/credentials.json")
        if not mymodel:
            raise AuthenticationFailed("You can't access google calendar because there is no calendar created yet")
        elif not mymodel.is_valid:
            raise AuthenticationFailed("You can't access google calendar because there is no calendar created yet")

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        # Initialize Google Calendar API service
        service = build("calendar", "v3", credentials=creds)
        # Refer to the Python quickstart on how to setup the environment:
        # https://developers.google.com/calendar/quickstart/python
        # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
        # stored credentials.
        pacific = pytz.timezone('Asia/Tehran')
        mymodel = PrincipalAddEvent.objects.create(start=request.data['start'], end=request.data['end'])
        mymodel.save()
        myid = mymodel.id
        newmode = PrincipalAddEvent.objects.filter(id=myid).first()
        nanay = pacific.localize(newmode.start)
        ended = newmode.end
        Strstarted = nanay.isoformat()
        Strended = ended.isoformat()
        myclassStudents = Student.objects.filter(School=school).all()
        emails = [{'email': student.Email} for student in myclassStudents]

        event = {
            'summary': request.data['flag'],
            'description': request.data['description'],
            'start': {
                'dateTime': Strstarted,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': Strended,
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': emails,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        # # Call the Calendar API
        # now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
        # print("Getting the upcoming 10 events")
        # events_result = (
        #     service.events()
        #     .list(
        #         calendarId="primary",
        #         timeMin=now,
        #         maxResults=10,
        #         singleEvents=True,
        #         orderBy="startTime",
        #     )
        #     .execute()
        # )
        # events = events_result.get("items", [])
        #
        #
        # # Prints the start and name of the next 10 events
        # for event in events:
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     print(start, event["summary"])
        # calendar_list = service.calendarList().list().execute()
        # primary_calendar = next((cal for cal in calendar_list['items'] if cal.get('primary')), None)
        # calendar_id = None
        # if primary_calendar:
        #     calendar_id =  primary_calendar['id']  # This is the calendar ID for the primary calendar
        # else:
        #     raise AuthenticationFailed("Primary calendar not found.")
        # calendar_url = f"https://calendar.google.com/calendar/u/0/r?cid="+str(calendar_id)
        # webbrowser.open(calendar_url)
        return Response({'message': 'Your event is now visible to students'})
