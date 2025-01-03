import datetime
from time import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.forms import BooleanField
from django.core.files.base import ContentFile
from rest_framework.views import APIView


class MyUserManager(BaseUserManager):
    def create_user(self, National_ID, first_name, last_name, username, Phone_Number, email, password=None):
        if not National_ID:
            raise ValueError('Users must have an National_ID')

        user = self.model(
            National_ID=National_ID,
            first_name=first_name,
            last_name=last_name,
            username=National_ID,
            Phone_Number=Phone_Number,
            email=email
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, National_ID, password=None):
        user = self.model(
            National_ID=National_ID
        )
        user.is_admin = True
        print(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=11, unique=True)
    National_ID = models.CharField(max_length=10, unique=True)


    USERNAME_FIELD = 'National_ID'
    REQUIRED_FIELDS = ['password']

    is_admin = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    objects = MyUserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.National_ID

class School(models.Model):
    SchoolType = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    EducationLevel = [
        ('primary', 'Primary'),
        ('middle', 'Middle'),
        ('high school', 'High School'),
    ]

    School_Name = models.CharField(max_length=60)
    Province = models.CharField(max_length=40)
    City = models.CharField(max_length=40)
    Address = models.CharField(max_length=100)
    School_Type = models.CharField(max_length=10, choices=SchoolType, blank=False)
    Education_Level = models.CharField(max_length=20, choices=EducationLevel, blank=False)
    Postal_Code = models.CharField(max_length=10, unique=True)
    Principal = models.ForeignKey(User, on_delete=models.CASCADE)


class SchoolProfile(models.Model):
    information = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='SchoolProfile')

class UserProfile(models.Model):
    bio = models.CharField(max_length=300, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfile')

class Student(models.Model):

    GradeLevel = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Father_Phone_Number = models.CharField(max_length=11, unique=True)
    LandLine = models.CharField(max_length=11, unique=True)
    Father_first_name = models.CharField(max_length=100)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100)
    Grade_Level = models.CharField(max_length=20, choices=GradeLevel, blank=False)
    National_ID = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)
    Parent_password = models.CharField(max_length=200)
    Email = models.EmailField()
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def get_email_field_name(self):
        return 'Email'



    USERNAME_FIELD = 'National_ID'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.National_ID

class StudentProfile(models.Model):
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentProfile')

class Teacher(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=11, unique=True)
    Address = models.CharField(max_length=100)
    National_ID = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)
    Email = models.EmailField()
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)


    def get_email_field_name(self):
        return 'Email'

    USERNAME_FIELD = 'National_ID'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.National_ID

class TeacherProfile(models.Model):
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='TeacherProfile')

class Classes(models.Model):
    Days = [
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
    ]

    Time = [
        ('8:00 to 9:00', '8:00 to 9:00'),
        ('9:15 to 10:15', '9:15 to 10:15'),
        ('10:30 to 11:30', '10:30 to 11:30'),
        ('11:45 to 12:45', '11:45 to 12:45'),
        ('13:00 to 14:00', '13:00 to 14:00'),
    ]
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Topic = models.CharField(max_length=30)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Session1Day = models.CharField(max_length=15, choices=Days, blank=False, null=False)
    Session1Time = models.CharField(max_length=20, choices=Time, blank=False, null=False)
    Session2Day = models.CharField(max_length=15, choices=Days, blank=True, null=True)
    Session2Time = models.CharField(max_length=20, choices=Time, blank=True, null=True)

class ClassStudent(models.Model):
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('Classes', 'Student')

class NotificationSchool(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)

class NotificationStudent(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)

class NotificationSchoolParent(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)

class NotificationParent(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)

class QuizTeacher(models.Model):
    Title = models.CharField(max_length=100)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    OpenTime = models.DateTimeField(blank=False, null=False)
    DurationHour = models.IntegerField()
    DurationMinute = models.IntegerField()
    Is_Published = models.BooleanField(default=False)

class QuizQuestion(models.Model):
    QuizTeacher = models.ForeignKey(QuizTeacher, on_delete=models.CASCADE)
    Question = models.TextField()
    Option1 = models.CharField(max_length=500)
    Option2 = models.CharField(max_length=500)
    Option3 = models.CharField(max_length=500)
    Option4 = models.CharField(max_length=500)
    Answer = models.IntegerField()
    Explanation = models.TextField()

class QuizQuestionStudent(models.Model):
    QuizQuestion = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    StudentAnswer = models.IntegerField()
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('QuizQuestion', 'Student')

class QuizStudentRecord(models.Model):
    QuizTeacher = models.ForeignKey(QuizTeacher, on_delete=models.CASCADE)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Degree = models.FloatField()
    FinishTime = models.DateTimeField()

class HallandAPI(models.Model):
    OnParticipation = models.IntegerField()
    Realistic = models.BooleanField()
    Investigative = models.BooleanField()
    Artistic = models.BooleanField()
    Social = models.BooleanField()
    Enterprising = models.BooleanField()
    Conventional = models.BooleanField()
    Time = models.DateTimeField(default=datetime.datetime.now)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)

class HomeWorkTeacher(models.Model):
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    Is_Published = models.BooleanField(default=False)
    Title = models.TextField()
    Description = models.TextField()
    file = models.FileField(upload_to='profile_image/', blank=True, null=True)
    DeadLine = models.DateTimeField(blank=False, null=False)

class HomeWorkStudent(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    HomeWorkAnswer = models.FileField(upload_to='profile_image/', blank=True, null=True)
    SendingTime = models.DateTimeField(default=datetime.datetime.now)
    HomeWorkTeacher = models.ForeignKey(HomeWorkTeacher, on_delete=models.CASCADE, related_name='HomeWorkStudent')
    Grade = models.IntegerField(null=True, blank=True)
    Graded = models.BooleanField(default=False)

class PrinicipalCalendar(models.Model):
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    gtoken = models.FileField(upload_to='profile_image/', blank=True, null=True)
    is_valid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the instance is being created (no primary key yet)
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save the instance first to get a valid primary key
        if is_new and not self.gtoken:
            # Save an empty token.json file after the instance is saved
            self.gtoken.save('token.json', ContentFile(''))

class SchoolTeachers(models.Model):
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('School', 'Teacher')

class StudentAttendance(models.Model):
    ClassStudent = models.ForeignKey(ClassStudent, on_delete=models.CASCADE)
    Date = models.DateField()
    Absent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('ClassStudent', 'Date')

class DisciplinaryScore(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Grade = models.IntegerField()

class DisciplinaryCase(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Case = models.CharField(max_length=500)

class ECFile(models.Model):
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    file = models.FileField(upload_to='profile_image/', blank=True, null=True)
    Title = models.CharField(max_length=500,blank=True, null=True)

class ECVideo(models.Model):
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    src = models.CharField(max_length=500,blank=True, null=True)
    Title = models.CharField(max_length=500,blank=True, null=True)

class StudentPlanning(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    StartDate = models.DateTimeField()
    Title =models.CharField(max_length=50)
    Duration =models.IntegerField()
    Explanation = models.CharField(max_length=50)
    feedbackCount = models.IntegerField(default=0)

class TeacherFeedback(models.Model):
    StudentPlanning = models.ForeignKey(StudentPlanning, on_delete=models.CASCADE)
    Feedback = models.CharField(max_length=500)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
class PrincipalAddEvent(models.Model):
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

class Message(models.Model):
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    message = models.TextField()

class QuizTeacherExplan(models.Model):
    Title = models.CharField(max_length=100)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    OpenTime = models.DateTimeField(blank=False, null=False)
    DurationHour = models.IntegerField()
    DurationMinute = models.IntegerField()
    Is_Published = models.BooleanField(default=False)

class QuizQuestionExplan(models.Model):
    QuizTeacherExplan = models.ForeignKey(QuizTeacherExplan, on_delete=models.CASCADE)
    Question = models.CharField(max_length=1000)
    Answer = models.CharField(max_length=1000)
    Zarib = models.FloatField()

class QuizQuestionStudentExplan(models.Model):
    QuizQuestionExplan = models.ForeignKey(QuizQuestionExplan, on_delete=models.CASCADE)
    StudentAnswer = models.CharField(max_length=1000)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Correctness = models.FloatField(default=0)
    Correctness100 = models.FloatField(default=0)
    marked = models.IntegerField(default=0)
    class Meta:
        unique_together = ('QuizQuestionExplan', 'Student')

class QuizStudentRecordExplan(models.Model):
    QuizTeacherExplan = models.ForeignKey(QuizTeacherExplan, on_delete=models.CASCADE)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Degree100 = models.FloatField()
    DegreeBarom = models.FloatField()
    FinishTime = models.DateTimeField()
    marked = models.IntegerField(default=0)

class Wallet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='wallet')
    balance = models.FloatField(default=0.00)

    def __str__(self):
        return f"Wallet for {self.student.first_name} {self.student.last_name}"

class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for {self.wallet.student.National_ID}"

class Fee(models.Model):
    Amount = models.FloatField()
    Year = models.IntegerField()
    Month = models.IntegerField()
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Is_Sent = models.IntegerField(default=0)
    class Meta:
        unique_together = ('Year', 'Month', 'School')

class FeePaid(models.Model):
    Fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Is_Paid = models.IntegerField(default=0)

class OnlineClass(models.Model):
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)