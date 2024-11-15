from rest_framework import serializers
from .models import User, Student, Teacher, School, Classes, ClassStudent
import re
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'National_ID', 'Phone_Number', 'password', 'password2']

    def validate(self, attrs):
        otherStudent = Student.objects.filter(National_ID=attrs['National_ID']).first()
        if otherStudent:
            raise serializers.ValidationError("An student registered with this National ID")

        otherTeacher = Teacher.objects.filter(National_ID=attrs['National_ID']).first()
        if otherTeacher:
            raise serializers.ValidationError("A teacher registered with this National ID")

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields do not match.'}
            )
        if not re.match('^[0-9]{10}$', attrs['National_ID']):
            raise serializers.ValidationError(
                {'National_ID': 'National ID must contain exactly 10 digits.'}
            )
        if not re.match('^[0-9]{11}$', attrs['Phone_Number']):
            raise serializers.ValidationError(
                {'Phone_Number': 'Phone number must contain exactly 11 digits.'}
            )
        if not attrs.get('first_name'):
            raise serializers.ValidationError(
                {'first_name': 'First name cannot be empty.'}
            )
        if not attrs.get('last_name'):
            raise serializers.ValidationError(
                {'last_name': 'Last name cannot be empty.'}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['National_ID'],
            National_ID=validated_data['National_ID'],
            Phone_Number=validated_data['Phone_Number']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class StudentSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'National_ID', 'Father_Phone_Number',
                  'Father_first_name', 'Father_last_name', 'Grade_Level', 'password',
                  'password2', 'Address', 'LandLine']

    def validate(self, attrs):
        otherPrincipal = User.objects.filter(National_ID=attrs['National_ID']).first()
        if otherPrincipal:
            raise serializers.ValidationError("A principal registered with this National ID")

        otherTecaher = Teacher.objects.filter(National_ID=attrs['National_ID']).first()
        if otherTecaher:
            raise serializers.ValidationError("A teacher registered with this National ID")

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields do not match.'}
            )
        if not re.match('^[0-9]{10}$', attrs['National_ID']):
            raise serializers.ValidationError(
                {'National_ID': 'National ID must contain exactly 10 digits.'}
            )
        if not re.match('^[0-9]{11}$', attrs['Father_Phone_Number']):
            raise serializers.ValidationError(
                {'Father_Phone_Number': 'Phone number must contain exactly 11 digits.'}
            )
        if not re.match('^[0-9]{11}$', attrs['LandLine']):
            raise serializers.ValidationError(
                {'LandLine': 'LandLine must contain exactly 11 digits.'}
            )
        if not attrs.get('first_name'):
            raise serializers.ValidationError(
                {'first_name': 'First name cannot be empty.'}
            )
        if not attrs.get('last_name'):
            raise serializers.ValidationError(
                {'last_name': 'Last name cannot be empty.'}
            )
        if not attrs.get('Father_first_name'):
            raise serializers.ValidationError(
                {'first_name': 'Father\'s First name cannot be empty.'}
            )
        if not attrs.get('Father_last_name'):
            raise serializers.ValidationError(
                {'last_name': 'Father\'s Last name cannot be empty.'}
            )
        if not attrs.get('Grade_Level'):
            raise serializers.ValidationError(
                {'Grade_Level': 'grade level must be selected.'}
            )
        if not attrs.get('Address'):
            raise serializers.ValidationError(
                {'Address': 'Address cannot be empty.'}
            )

        return attrs

    def create(self, validated_data):
        student = Student.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            National_ID=validated_data['National_ID'],
            Father_Phone_Number=validated_data['Father_Phone_Number'],
            LandLine =validated_data['LandLine'],
            Father_first_name=validated_data['Father_first_name'],
            Father_last_name=validated_data['Father_last_name'],
            Address=validated_data['Address'],
            Grade_Level=validated_data['Grade_Level'],
            password=make_password(validated_data['password']),
        )
        student.save()

        return student

class TeacherSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'National_ID', 'Phone_Number',
                  'password', 'password2', 'Address']

    def validate(self, attrs):
        otherPrincipal = User.objects.filter(National_ID=attrs['National_ID']).first()
        if otherPrincipal:
            raise serializers.ValidationError("A principal registered with this National ID")

        otherStudent = Student.objects.filter(National_ID=attrs['National_ID']).first()
        if otherStudent:
            raise serializers.ValidationError("A student registered with this National ID")

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields do not match.'}
            )
        if not re.match('^[0-9]{10}$', attrs['National_ID']):
            raise serializers.ValidationError(
                {'National_ID': 'National ID must contain exactly 10 digits.'}
            )
        if not re.match('^[0-9]{11}$', attrs['Phone_Number']):
            raise serializers.ValidationError(
                {'Phone_Number': 'Phone number must contain exactly 11 digits.'}
            )
        if not attrs.get('first_name'):
            raise serializers.ValidationError(
                {'first_name': 'First name cannot be empty.'}
            )
        if not attrs.get('last_name'):
            raise serializers.ValidationError(
                {'last_name': 'Last name cannot be empty.'}
            )
        if not attrs.get('Address'):
            raise serializers.ValidationError(
                {'Address': 'Address cannot be empty.'}
            )

        return attrs

    def create(self, validated_data):
        teacher = Teacher.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            National_ID=validated_data['National_ID'],
            Phone_Number=validated_data['Phone_Number'],
            Address=validated_data['Address'],
            password=make_password(validated_data['password']),
        )
        teacher.save()

        return teacher

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'School_Name', 'School_Type', 'Education_Level', 'Province',
                  'City', 'Address', 'Postal_Code', 'Principal']

    def validate(self, attrs):
        if not attrs.get('School_Type'):
            raise serializers.ValidationError(
                {'School_Type': 'School type must be selected.'}
            )
        if not attrs.get('Education_Level'):
            raise serializers.ValidationError(
                {'Education_Level': 'Education level must be selected.'}
            )
        if not attrs.get('Province'):
            raise serializers.ValidationError(
                {'Province': 'Province cannot be empty.'}
            )
        if not attrs.get('City'):
            raise serializers.ValidationError(
                {'City': 'City cannot be empty.'}
            )
        if not attrs.get('Address'):
            raise serializers.ValidationError(
                {'Address': 'Address cannot be empty.'}
            )

        return attrs

    def create(self, validated_data):
        school = School.objects.create(
            School_Name=validated_data['School_Name'],
            Province=validated_data['Province'],
            City=validated_data['City'],
            Address=validated_data['Address'],
            School_Type=validated_data['School_Type'],
            Education_Level=validated_data['Education_Level'],
            Postal_Code=validated_data['Postal_Code'],
            Principal=validated_data['Principal']
        )
        school.save()

        return school

class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classes
        fields = ['id', 'School', 'Topic', 'Teacher', 'Session1Day',
                  'Session2Day', 'Session1Time', 'Session2Time']

    def validate(self, attrs):
        if not attrs.get('School'):
            raise serializers.ValidationError(
                {'School': 'School must be selected.'}
            )
        if not attrs.get('Topic'):
            raise serializers.ValidationError(
                {'Topic': 'Topic must be selected.'}
            )
        if not attrs.get('Teacher'):
            raise serializers.ValidationError(
                {'Teacher': 'Teacher cannot be empty.'}
            )
        if not attrs.get('Session1Day'):
            raise serializers.ValidationError(
                {'Session1Day': 'Session1Day cannot be empty.'}
            )
        if not attrs.get('Session1Time'):
            raise serializers.ValidationError(
                {'Session1Time': 'Session1Time cannot be empty.'}
            )

        return attrs

    def create(self, validated_data):
        myclass = Classes.objects.create(
            School=validated_data['School'],
            Topic=validated_data['Topic'],
            Teacher=validated_data['Teacher'],
            Session1Day=validated_data['Session1Day'],
            Session2Day=validated_data['Session2Day'],
            Session1Time=validated_data['Session1Time'],
            Session2Time=validated_data['Session2Time'],
        )
        myclass.save()

        return myclass

class ClassStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'Classes', 'Student']

    def validate(self, attrs):
        if not attrs.get('Classes'):
            raise serializers.ValidationError(
                {'School_Type': 'School type must be selected.'}
            )
        if not attrs.get('Student'):
            raise serializers.ValidationError(
                {'Student': 'Student must be selected.'}
            )

        return attrs

    def create(self, validated_data):
        myclass = ClassStudent.objects.create(
            School=validated_data['School'],
            Student=validated_data['Student'],
        )
        myclass.save()

        return myclass