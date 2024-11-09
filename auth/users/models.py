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
    # username = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
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