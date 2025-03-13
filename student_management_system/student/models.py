from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.CharField(max_length=20, blank=True, null=True, unique=True)

class Student(models.Model):
    teacher = models.ForeignKey(CustomUser, limit_choices_to={'is_teacher': True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='students/')
    user_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
User = get_user_model()
class Assignment(models.Model):
    teacher = models.ForeignKey(CustomUser, limit_choices_to={'is_teacher': True}, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)  # Assign to a specific student
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='assignments/')  # Teacher's uploaded assignment
    uploaded_at = models.DateTimeField(auto_now_add=True)
    student_submission = models.FileField(upload_to='submissions/', blank=True, null=True)  # Student's answer file
    submitted_at = models.DateTimeField(blank=True, null=True)
    marks = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f"{self.title} - {self.student.name}"
