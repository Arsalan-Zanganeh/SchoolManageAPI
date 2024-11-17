from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, National_ID, first_name, last_name, username, Phone_Number, password=None):
        if not National_ID:
            raise ValueError('Users must have an National_ID')

        user = self.model(
            National_ID=National_ID,
            first_name=first_name,
            last_name=last_name,
            username=National_ID,
            Phone_Number=Phone_Number
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
    # SchoolType = [
    #     ('public', 'Public'),
    #     ('private', 'Private'),
    # ]
    #
    # EducationLevel = [
    #     ('primary', 'Primary'),
    #     ('middle', 'Middle'),
    #     ('high school', 'High School'),
    # ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=11, unique=True)
    # School_Name = models.CharField(max_length=60)
    # Province = models.CharField(max_length=40)
    # City = models.CharField(max_length=40)
    # Address = models.CharField(max_length=100)
    # School_Type = models.CharField(max_length=10, choices=SchoolType, blank=False)
    # Education_Level = models.CharField(max_length=20, choices=EducationLevel, blank=False)
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
    Father_last_name = models.CharField(max_length=100)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100)
    Grade_Level = models.CharField(max_length=20, choices=GradeLevel, blank=False)
    National_ID = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)


    USERNAME_FIELD = 'National_ID'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.National_ID

class Teacher(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=11, unique=True)
    Address = models.CharField(max_length=100)
    National_ID = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)

    USERNAME_FIELD = 'National_ID'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.National_ID

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