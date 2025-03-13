from django.contrib import admin
from .models import Student, CustomUser

# Register CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_teacher", "is_student", "user_id") 

# Register Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "teacher", "user_id")  
    search_fields = ("name", "email", "user_id")
    list_filter = ("teacher",)
