from django.db import models
from users.models import User,Teacher,Student
from django.core.exceptions import ValidationError
from users.models import Classes

class AccountForChat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    account_type = models.CharField(max_length=10, choices=[('manager', 'Manager'), ('teacher', 'Teacher'), ('student', 'Student')])
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.account_type == 'teacher' and self.student:
            raise ValidationError('A teacher cannot be a student.')
        if self.account_type == 'student' and self.teacher:
            raise ValidationError('A student cannot be a teacher.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Chat(models.Model):
    title = models.CharField(max_length=200)
    participants = models.ManyToManyField(AccountForChat, related_name='chats')
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(AccountForChat, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']