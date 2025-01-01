from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import StudentSerializer, ClassSerializer, ParentHomeworkSerializer, \
    ParentQuizRecordSerializer, AttendanceParentSerializer, ParentDisciplinaryCaseSerializer, \
    ParentDisciplinaryScoreSerializer, RecentQuizTestSerializer, RecentHomeworkSerializer, \
    ParentWalletSerializer, FeeSerializer, FeeListParentSerializer
from users.models import Student, ClassStudent, Classes, HomeWorkStudent, QuizStudentRecord, \
    StudentAttendance, DisciplinaryCase, DisciplinaryScore, QuizTeacher, QuizTeacherExplan, \
    QuizStudentRecordExplan, HomeWorkTeacher, Wallet, WalletTransaction, School, Fee, FeePaid
import jwt, datetime
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.
class StudentLoginView(APIView):
    def post(self, request):
        National_ID = request.data['National_ID']
        password = request.data['password']
        user = Student.objects.filter(National_ID=National_ID).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Wrong password!")

        payload = {
            'National_ID': user.National_ID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
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

class StudentView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = Student.objects.filter(National_ID=payload['National_ID']).first()
        serializer = StudentSerializer(user)

        return Response(serializer.data)

class StudentLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You have been logged out.'
        }

        return response

class StudentClassesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        classes = ClassStudent.objects.filter(Student=student).values_list('Classes__pk', flat=True).all()
        if not classes:
            raise AuthenticationFailed("Student not found!")
        fullClasses = Classes.objects.filter(pk__in=classes).all()
        if not fullClasses:
            raise AuthenticationFailed("Students not found!")

        serializer = ClassSerializer(fullClasses, many=True)
        return Response(serializer.data)

class ParentLogin(APIView):
    def post(self, request):
        National_ID = request.data['National_ID']
        password = request.data['Parent_password']
        user = Student.objects.filter(National_ID=National_ID).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not check_password(password, user.Parent_password):
            raise AuthenticationFailed("Wrong password!")

        payload = {
            'National_ID': user.National_ID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
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

class ParentLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You have been logged out.'
        }
        return response

class ParentClassesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        classes = ClassStudent.objects.filter(Student=student).values_list('Classes__pk', flat=True).all()
        if not classes:
            raise AuthenticationFailed("Student not found!")
        fullClasses = Classes.objects.filter(pk__in=classes).all()
        if not fullClasses:
            raise AuthenticationFailed("Students not found!")

        serializer = ClassSerializer(fullClasses, many=True)
        return Response(serializer.data)

class ParentEnterClass(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")

        payload = {
            'Class_ID': request.data['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithm='HS256')

        response = Response()

        response.set_cookie(key='class', value=token, httponly=True)
        # response.set_cookie(key='class', value=token, httponly=True, samesite='None', secure=True)
        response.data = {
            'class': token
        }

        return response

class ParentSeeHomeworkRecords(APIView):
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
            raise AuthenticationFailed("There is no such a student")

        token = request.COOKIES.get('class')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        homeworks = HomeWorkStudent.objects.filter(Student=student, HomeWorkTeacher__Classes=myclass).all()
        serializer = ParentHomeworkSerializer(homeworks, many=True)
        return Response(serializer.data)

class ParentCheckStudentAttendance(APIView):
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
            raise AuthenticationFailed("There is no such a student")

        token = request.COOKIES.get('class')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = StudentAttendance.objects.filter(ClassStudent__Student=student, ClassStudent__Classes=myclass).all()
        serializer = AttendanceParentSerializer(obj, many=True)
        return Response(serializer.data)

class ParentShowQuizRecords(APIView):
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
            raise AuthenticationFailed("There is no such a student")

        token = request.COOKIES.get('class')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        # quiz = QuizTeacher.objects.filter(id=request.data['QuizTeacher_ID']).first()
        # if not quiz:
        #     raise AuthenticationFailed("There is no such a quiz")
        # noww = datetime.datetime.now()
        # validAfter = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
        # if noww < quiz.OpenTime:
        #     raise AuthenticationFailed("Exam is not started yet")
        # if noww > validAfter:
        #     records = QuizStudentRecord.objects.filter(QuizTeacher = quiz, Student=student).first()
        #     if not records:
        #         raise AuthenticationFailed("There is no such a record")
        #     serializer = StudentQuizRecordSerializer(records)
        #     return Response(serializer.data)
        records = QuizStudentRecord.objects.filter(Student=student, QuizTeacher__Classes=myclass).all()
        wanted = []
        now = datetime.datetime.now()
        for record in records:
            quiz = record.QuizTeacher
            validAfter = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
            print(validAfter)
            print(now)
            if now > validAfter:
                wanted.append(record)
        serializer = ParentQuizRecordSerializer(wanted, many=True)
        return Response(serializer.data)

class DisciplinaryCaseList(APIView):
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
            raise AuthenticationFailed("There is no such a parent")

        damn = DisciplinaryCase.objects.filter(Student=student).all()
        serializer = ParentDisciplinaryCaseSerializer(damn, many=True)
        return Response(serializer.data)

class DisciplineScore(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        damn = DisciplinaryScore.objects.filter(Student=student).first()
        serializer = ParentDisciplinaryScoreSerializer(damn)
        return Response(serializer.data)

class RecentQuizTest(APIView):
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
            raise AuthenticationFailed("There is no such a student")

        mylist = []
        noww = datetime.datetime.now()
        myvals = ClassStudent.objects.filter(Student=student).values_list('Classes__id', flat=True)
        myquizes = QuizTeacher.objects.filter(Classes__id__in=myvals, Is_Published=True).all()
        print(myquizes)
        for quiz in myquizes:
            endtime = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
            print(endtime)
            if endtime > noww:
                myrecord = QuizStudentRecord.objects.filter(Student=student, QuizTeacher=quiz).first()
                if not myrecord:
                    mylist.append(quiz)

        serializer = RecentQuizTestSerializer(mylist, many=True)
        return Response(serializer.data)

class RecentQuizExplan(APIView):
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
            raise AuthenticationFailed("There is no such a student")
        mylist = []
        noww = datetime.datetime.now()
        myvals = ClassStudent.objects.filter(Student=student).values_list('Classes__id', flat=True)
        myquizes = QuizTeacherExplan.objects.filter(Classes__id__in=myvals, Is_Published=True).all()
        for quiz in myquizes:
            endtime = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
            if endtime > noww:
                myrecord = QuizStudentRecordExplan.objects.filter(Student=student, QuizTeacherExplan=quiz).first()
                if not myrecord:
                    mylist.append(quiz)

        serializer = RecentQuizTestSerializer(mylist, many=True)
        return Response(serializer.data)

class RecentHomework(APIView):
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
            raise AuthenticationFailed("There is no such a student")
        mylist = []
        noww = datetime.datetime.now()
        myvals = ClassStudent.objects.filter(Student=student).values_list('Classes__id', flat=True)
        myhomeworks = HomeWorkTeacher.objects.filter(Classes__id__in=myvals, Is_Published=True).all()
        for homework in myhomeworks:
            if homework.DeadLine > noww:
                myrecord = HomeWorkStudent.objects.filter(Student=student, HomeWorkTeacher=homework).first()
                if not myrecord.HomeWorkAnswer:
                    mylist.append(homework)

        serializer = RecentHomeworkSerializer(mylist, many=True)
        return Response(serializer.data)


class ChargeWalletView(APIView):
    def post(self, request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:

            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        if not student:
            raise AuthenticationFailed("Student not found.")

        wallet = Wallet.objects.filter(student=student).first()

        if not wallet:
            raise AuthenticationFailed("Wallet not found for this student.")

        amount = float(request.data.get('amount'))

        if amount <= 0:
            return Response({"message": "Amount must be greater than zero."}, status=400)

        wallet.balance += amount
        wallet.save()

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='credit',
            balance_after_transaction=wallet.balance
        )

        serializer = ParentWalletSerializer(wallet)
        return Response(serializer.data)


class DebitWalletView(APIView):
    def post(self, request):
        # Retrieve JWT token from cookies
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the JWT token to extract the user information (e.g., National_ID of the manager)
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        if not student:
            raise AuthenticationFailed("Student not found.")

        # if not manager.is_admin:
        #     raise AuthenticationFailed("You do not have permission to perform this action.")

        wallet = Wallet.objects.filter(student=student).first()

        if not wallet:
            raise AuthenticationFailed("Wallet not found for this student.")

        amount = float(request.data.get('amount'))

        # Validate the amount
        if amount <= 0:
            return Response({"message": "Amount must be greater than zero."}, status=400)

        if amount > wallet.balance:
            return Response({"message": "Insufficient balance in the wallet."}, status=400)

        wallet.balance -= amount
        wallet.save()

        # Log the transaction in the WalletTransaction model
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='debit',
            balance_after_transaction=wallet.balance
        )

        # Serialize the student data and return it in the response
        serializer = ParentWalletSerializer(wallet)
        return Response(serializer.data)


class WalletView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the JWT token to extract the user information (e.g., National_ID of the manager)
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        if not student:
            raise AuthenticationFailed("Student not found.")

        wallet = Wallet.objects.filter(student=student).first()

        if not wallet:
            raise AuthenticationFailed("Wallet not found for this student.")

        serializer = ParentWalletSerializer(wallet)

        return Response(serializer.data)

class PrincipalAddChangeFee(APIView):
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

        myfee = Fee.objects.filter(School=school, Year=request.data['Year'], Month=request.data['Month']).first()
        if myfee:
            if myfee.Is_Sent == 1:
                return Response({"message": "Fee already sent"})
            myfee.Year = request.data['Year']
            myfee.Month = request.data['Month']
            myfee.Amount = request.data['Amount']
            myfee.save()
            return Response({"message": "Fee changed"})

        myfee = Fee.objects.create(School=school, Year=request.data['Year'], Month=request.data['Month'], Amount=request.data['Amount'])
        myfee.save()
        return Response({"message": "Fee added"})

class PrincipalSendFee(APIView):
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

        myfee = Fee.objects.filter(School=school, id=request.data['id']).first()
        if not myfee:
            raise AuthenticationFailed("Fee not found.")

        if myfee.Is_Sent == 1:
            return Response({"message": "Fee already sent"})

        myfee.Is_Sent = 1
        myfee.save()

        students = Student.objects.filter(School=school).all()
        for student in students:
            studentfee = FeePaid.objects.create(Student=student, Fee=myfee)
            studentfee.save()
        return Response({"message": "Fee sent"})

class PrincipalFeeList(APIView):
    def get(self, request):
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

        myfee = Fee.objects.filter(School=school).all()
        serializer = FeeSerializer(myfee, many=True)
        return Response(serializer.data)

class PrincipalFeePaidList(APIView):
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

        fees = FeePaid.objects.filter(Student__School=school).all()
        serializer = FeeListParentSerializer(fees, many=True)
        return Response(serializer.data)

class ParentFeeList(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the JWT token to extract the user information (e.g., National_ID of the manager)
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        if not student:
            raise AuthenticationFailed("Student not found.")

        fees = FeePaid.objects.filter(Student=student).all()
        serializer = FeeListParentSerializer(fees, many=True)
        return Response(serializer.data)

class ParentPayFee(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Decode the JWT token to extract the user information (e.g., National_ID of the manager)
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        if not student:
            raise AuthenticationFailed("Student not found.")

        fee = FeePaid.objects.filter(Student=student, id=request.data['id']).first()
        if not fee:
            raise AuthenticationFailed("Fee not found.")

        if fee.Is_Paid == 1:
            return Response({"message": "Fee already paid"})

        wallet = Wallet.objects.filter(student=student).first()

        if not wallet:
            raise AuthenticationFailed("Wallet not found for this student.")

        if wallet.balance<fee.Fee.Amount:
            return Response({"message": "Not enough money"})

        wallet.balance -= fee.Fee.Amount
        wallet.save()
        fee.Is_Paid = 1
        fee.save()
        return Response({"message": "Fee paid"})