from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student

SECRET_KEY = "hello"

class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student')
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)
    secret_key = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'secret_key']

class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_id = forms.CharField(required=False)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'address', 'photo', 'user_id']


from django import forms
from .models import Assignment, Student

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['student', 'title', 'pdf']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)  # Get teacher from the view
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['student'].queryset = Student.objects.filter(teacher=teacher)  # Filter students
        self.fields['student'].label_from_instance = lambda obj: obj.user_id  # Show USN instead of name
        
        
from django import forms
from .models import Assignment

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['student_submission']
