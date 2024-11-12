from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    SchoolType = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    EducationLevel = [
        ('primary', 'Primary'),
        ('middle', 'Middle'),
        ('high school', 'High School'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=11, unique=True)
    School_Name = models.CharField(max_length=60)
    Province = models.CharField(max_length=40)
    City = models.CharField(max_length=40)
    Address = models.CharField(max_length=100)
    School_Type = models.CharField(max_length=10, choices=SchoolType, blank=False)
    Education_Level = models.CharField(max_length=20, choices=EducationLevel, blank=False)
    National_ID = models.CharField(max_length=10, unique=True)


    USERNAME_FIELD = 'National_ID'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username

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
    # School_Name = models.CharField(max_length=60)
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