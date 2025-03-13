from django.urls import path
from .views import register, login_view, teacher_dashboard, student_dashboard, add_student,upload_assignment,logout_view,delete_student,edit_student
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/<str:student_id>/', student_dashboard, name='student_dashboard'),
    path('add-student/', add_student, name='add_student'),
    path('delete-student/<int:student_id>/', delete_student, name='delete_student'),
    path('edit-student/<int:student_id>/', edit_student, name='edit_student'),
    



]
