# Generated by Django 5.1.3 on 2025-01-02 03:02

import datetime
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Topic', models.CharField(max_length=30)),
                ('Session1Day', models.CharField(choices=[('saturday', 'Saturday'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday')], max_length=15)),
                ('Session1Time', models.CharField(choices=[('8:00 to 9:00', '8:00 to 9:00'), ('9:15 to 10:15', '9:15 to 10:15'), ('10:30 to 11:30', '10:30 to 11:30'), ('11:45 to 12:45', '11:45 to 12:45'), ('13:00 to 14:00', '13:00 to 14:00')], max_length=20)),
                ('Session2Day', models.CharField(blank=True, choices=[('saturday', 'Saturday'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday')], max_length=15, null=True)),
                ('Session2Time', models.CharField(blank=True, choices=[('8:00 to 9:00', '8:00 to 9:00'), ('9:15 to 10:15', '9:15 to 10:15'), ('10:30 to 11:30', '10:30 to 11:30'), ('11:45 to 12:45', '11:45 to 12:45'), ('13:00 to 14:00', '13:00 to 14:00')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrincipalAddEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('Phone_Number', models.CharField(max_length=11, unique=True)),
                ('Address', models.CharField(max_length=100)),
                ('National_ID', models.CharField(max_length=10, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('Phone_Number', models.CharField(max_length=11, unique=True)),
                ('National_ID', models.CharField(max_length=10, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ECFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='profile_image/')),
                ('Title', models.CharField(blank=True, max_length=500, null=True)),
                ('Classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
            ],
        ),
        migrations.CreateModel(
            name='ECVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(blank=True, max_length=500, null=True)),
                ('Title', models.CharField(blank=True, max_length=500, null=True)),
                ('Classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
            ],
        ),
        migrations.CreateModel(
            name='HomeWorkTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Is_Published', models.BooleanField(default=False)),
                ('Title', models.TextField()),
                ('Description', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='profile_image/')),
                ('DeadLine', models.DateTimeField()),
                ('Classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
                ('Teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('Classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
            ],
        ),
        migrations.CreateModel(
            name='QuizTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100)),
                ('OpenTime', models.DateTimeField()),
                ('DurationHour', models.IntegerField()),
                ('DurationMinute', models.IntegerField()),
                ('Is_Published', models.BooleanField(default=False)),
                ('Classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
                ('Teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.TextField()),
                ('Option1', models.CharField(max_length=500)),
                ('Option2', models.CharField(max_length=500)),
                ('Option3', models.CharField(max_length=500)),
                ('Option4', models.CharField(max_length=500)),
                ('Answer', models.IntegerField()),
                ('Explanation', models.TextField()),
                ('QuizTeacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizteacher')),
            ],
        ),
        migrations.CreateModel(
            name='QuizTeacherExplan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100)),
                ('OpenTime', models.DateTimeField()),
                ('DurationHour', models.IntegerField()),
                ('DurationMinute', models.IntegerField()),
                ('Is_Published', models.BooleanField(default=False)),
                ('Classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
                ('Teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestionExplan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.CharField(max_length=1000)),
                ('Answer', models.CharField(max_length=1000)),
                ('Zarib', models.FloatField()),
                ('QuizTeacherExplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizteacherexplan')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('School_Name', models.CharField(max_length=60)),
                ('Province', models.CharField(max_length=40)),
                ('City', models.CharField(max_length=40)),
                ('Address', models.CharField(max_length=100)),
                ('School_Type', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=10)),
                ('Education_Level', models.CharField(choices=[('primary', 'Primary'), ('middle', 'Middle'), ('high school', 'High School')], max_length=20)),
                ('Postal_Code', models.CharField(max_length=10, unique=True)),
                ('Principal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrinicipalCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gtoken', models.FileField(blank=True, null=True, upload_to='profile_image/')),
                ('is_valid', models.BooleanField(default=False)),
                ('School', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationSchoolParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('archive', models.BooleanField(default=False)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('archive', models.BooleanField(default=False)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school')),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.FloatField()),
                ('Year', models.IntegerField()),
                ('Month', models.IntegerField()),
                ('Is_Sent', models.IntegerField(default=0)),
                ('School', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school')),
            ],
            options={
                'unique_together': {('Year', 'Month', 'School')},
            },
        ),
        migrations.AddField(
            model_name='classes',
            name='School',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school'),
        ),
        migrations.CreateModel(
            name='SchoolProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information', models.TextField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image/')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SchoolProfile', to='users.school')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('Father_Phone_Number', models.CharField(max_length=11, unique=True)),
                ('LandLine', models.CharField(max_length=11, unique=True)),
                ('Father_first_name', models.CharField(max_length=100)),
                ('Address', models.CharField(max_length=100)),
                ('Grade_Level', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=20)),
                ('National_ID', models.CharField(max_length=10, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('Parent_password', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('School', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school')),
            ],
        ),
        migrations.CreateModel(
            name='QuizStudentRecordExplan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Degree100', models.FloatField()),
                ('DegreeBarom', models.FloatField()),
                ('FinishTime', models.DateTimeField()),
                ('marked', models.IntegerField(default=0)),
                ('QuizTeacherExplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizteacherexplan')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='QuizStudentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Degree', models.FloatField()),
                ('FinishTime', models.DateTimeField()),
                ('QuizTeacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizteacher')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('archive', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('archive', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='HomeWorkStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HomeWorkAnswer', models.FileField(blank=True, null=True, upload_to='profile_image/')),
                ('SendingTime', models.DateTimeField(default=datetime.datetime.now)),
                ('Grade', models.IntegerField(blank=True, null=True)),
                ('Graded', models.BooleanField(default=False)),
                ('HomeWorkTeacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='HomeWorkStudent', to='users.homeworkteacher')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='HallandAPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OnParticipation', models.IntegerField()),
                ('Realistic', models.BooleanField()),
                ('Investigative', models.BooleanField()),
                ('Artistic', models.BooleanField()),
                ('Social', models.BooleanField()),
                ('Enterprising', models.BooleanField()),
                ('Conventional', models.BooleanField()),
                ('Time', models.DateTimeField(default=datetime.datetime.now)),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='FeePaid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Is_Paid', models.IntegerField(default=0)),
                ('Fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.fee')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaryScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Grade', models.IntegerField()),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaryCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Case', models.CharField(max_length=500)),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='ClassStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'unique_together': {('Classes', 'Student')},
            },
        ),
        migrations.CreateModel(
            name='StudentPlanning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartDate', models.DateTimeField()),
                ('Title', models.CharField(max_length=50)),
                ('Duration', models.IntegerField()),
                ('Explanation', models.CharField(max_length=50)),
                ('feedbackCount', models.IntegerField(default=0)),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image/')),
                ('bio', models.TextField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StudentProfile', to='users.student')),
            ],
        ),
        migrations.AddField(
            model_name='classes',
            name='Teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher'),
        ),
        migrations.CreateModel(
            name='TeacherFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Feedback', models.CharField(max_length=500)),
                ('StudentPlanning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.studentplanning')),
                ('Teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image/')),
                ('bio', models.TextField(blank=True, null=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TeacherProfile', to='users.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=300, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserProfile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(default=0.0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=6)),
                ('balance_after_transaction', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='users.wallet')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestionStudentExplan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudentAnswer', models.CharField(max_length=1000)),
                ('Correctness', models.FloatField(default=0)),
                ('Correctness100', models.FloatField(default=0)),
                ('marked', models.IntegerField(default=0)),
                ('QuizQuestionExplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizquestionexplan')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'unique_together': {('QuizQuestionExplan', 'Student')},
            },
        ),
        migrations.CreateModel(
            name='QuizQuestionStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudentAnswer', models.IntegerField()),
                ('QuizQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizquestion')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'unique_together': {('QuizQuestion', 'Student')},
            },
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Absent', models.BooleanField(default=False)),
                ('ClassStudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.classstudent')),
            ],
            options={
                'unique_together': {('ClassStudent', 'Date')},
            },
        ),
        migrations.CreateModel(
            name='SchoolTeachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('School', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school')),
                ('Teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
            options={
                'unique_together': {('School', 'Teacher')},
            },
        ),
    ]
