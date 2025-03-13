from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, StudentLoginForm, StudentForm,AssignmentForm,AssignmentSubmissionForm  
from .models import CustomUser, Student,Assignment
from django.contrib.auth.models import Group
from django.utils.timezone import now


SECRET_KEY = "hello"

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            user_id = form.cleaned_data.get('user_id', None)  # Get user_id from form

            if user_type == 'teacher':
                if form.cleaned_data['secret_key'] != SECRET_KEY:
                    form.add_error('secret_key', 'Invalid Secret Key')
                    return render(request, 'register.html', {'form': form})
                user.is_teacher = True
                user.is_superuser = True

            elif user_type == 'student':
                user.is_student = True

            if user_id:  # If user_id is provided manually, use it
                user.user_id = user_id
            else:
                user.save()  # Save first to generate a primary key
                user.user_id = f"U{user.pk}"  # Auto-generate if not provided

            user.save(update_fields=['user_id'])  # Save user_id

            return redirect('login')

    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_id = form.cleaned_data.get('user_id', None)

            # Fetch user from CustomUser using email
            user = CustomUser.objects.filter(email=email).first()

            if user and user.check_password(password):  # Validate password manually
                if user.is_teacher:
                   
                    login(request, user)
                    return redirect('teacher_dashboard')

                elif user.is_student:
                   
                    student = Student.objects.filter(user_id=user_id, email=email).first()
                    
                    if student:
                        login(request, user)
                        return redirect('student_dashboard', student_id=student.user_id)
                    else:
                        form.add_error('user_id', "Invalid User ID")

                else:
                    form.add_error(None, "User type not recognized")
            else:
                form.add_error(None, "Invalid credentials")

    else:
        form = StudentLoginForm()

    return render(request, 'login.html', {'form': form})



def teacher_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_teacher:
        return redirect('login')

    students = Student.objects.filter(teacher=request.user)  
    assignments = Assignment.objects.filter(teacher=request.user)  
    form = AssignmentForm()  
    students_count = students.count()  
    assignments_sent_count = assignments.count() 
    assignments_received_count = Assignment.objects.filter(student_submission__isnull=False, teacher=request.user).count()  # Count received assignments


   
    if request.method == 'POST':
        if 'assignment_id' in request.POST: 
            assignment_id = request.POST.get("assignment_id")
            marks = request.POST.get("marks")

            assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
            assignment.marks = int(marks)  
            assignment.save()
            return redirect('teacher_dashboard')

        else: 
            form = AssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                assignment = form.save(commit=False)
                assignment.teacher = request.user  
                assignment.save()
                return redirect('teacher_dashboard')

    return render(request, 'teacher_dashboard.html', {
        'students': students,
        'assignments': assignments,
        'form': form,
        'students_count': students_count,
        'assignments_sent_count': assignments_sent_count,
        'assignments_received_count': assignments_received_count,
    })


from .models import Student, Assignment
from .forms import AssignmentSubmissionForm  # Import the form

def student_dashboard(request, student_id):
    student = get_object_or_404(Student, user_id=student_id)
    assignments = Assignment.objects.filter(student=student)  

    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        assignment = Assignment.objects.get(id=assignment_id, student=student)
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=assignment)

        if form.is_valid():
            assignment.submitted_at = now()  # Set submission timestamp
            form.save()
            return redirect('student_dashboard', student_id=student_id)

    else:
        form = AssignmentSubmissionForm()

    return render(request, 'student_dashboard.html', {
        'student': student, 
        'assignments': assignments, 
        'form': form
    })


def add_student(request):
    if not request.user.is_authenticated or not request.user.is_teacher:
        return redirect('login')

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = request.user
            student.save()
            return redirect('teacher_dashboard')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

@login_required
def upload_assignment(request):
    if not request.user.is_teacher:
        return redirect('login') 
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, teacher=request.user)  
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm(teacher=request.user)  
    return render(request, 'upload_assignment.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  


def delete_student(request, student_id):
    if not request.user.is_teacher:
        return redirect('login') 

    student = get_object_or_404(Student, id=student_id, teacher=request.user)  
    student.delete()
    return redirect('teacher_dashboard')  

def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard', student_id=student.user_id)
    else:
        form = StudentForm(instance=student)

    return render(request, 'edit_student.html', {'form': form, 'student': student})