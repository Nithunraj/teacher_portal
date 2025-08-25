from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from .forms import UserForm, StudentForm
from .models import User, StudentDetails, AuditLog
from django.contrib import messages, auth
from .utils import verify_password, get_user_session, calculate_new_marks, hash_password
from django.contrib.auth.decorators import login_required
from functools import wraps

# Create your views here.
def log_in_audit(log_details):
    AuditLog.objects.create(
                user=log_details['user'],
                action=log_details['action'],
                student_name = log_details['student_name'],
                student_id=log_details['student_id'],
                details = log_details['details'],
            )
    return "Logged Successfully"

def superuser_login(request, username, password):
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        messages.success(request, "You are now logged in!")
        return '/admin/'
    else:
        messages.error(request, "Invalid login credentials")
        return 'login'
    
def session_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print("Checking session...")
        if not request.session.get('user_id'):
            return redirect('login')  # your login URL name
        print("Has session")
        return view_func(request, *args, **kwargs)
    return wrapper

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse("Invalid username or password")
        
        if user.is_superuser:
           redirect_val = superuser_login(request, username, password)
           return redirect(redirect_val)
        
        elif verify_password(user.password, password):
            request.session['user_id'] = user.id
            messages.success(request, "You are now logged in!")
            return redirect('dashboard')
    
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    return render(request, 'home.html')

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            hashed_password = hash_password(password)
            user = User.objects.create_user(username=username, email=email, password=hashed_password)
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('login')
    else:
        form = UserForm()
        context = {
            'form':form
        }
        print(form)
    return render(request, 'accounts/register.html', context)

def logout(request):
    request.session.flush()
    messages.info(request, 'You are logged out.')
    return redirect('home')

@never_cache
@session_login_required
def dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    # students = StudentDetails.objects.filter(user=user)
    students = StudentDetails.objects.all()
    student_details = StudentForm()

    context = {
        'students' : students,
        'student_details' : student_details
    }
    return render(request, 'accounts/dashboard.html', context)

def add_student(request):
    user_id = get_user_session(request)
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        name = request.POST['name'].strip().title() 
        subject = request.POST['subject'].strip().title()
        mark = request.POST['mark']

        print(name)
        student = StudentDetails.objects.filter(name__iexact=name, subject__iexact=subject)
        if student.exists():
            for data in student:
                student_id = data.id
                previous_mark = data.mark
                mark_calculation, updated_mark = calculate_new_marks(mark, previous_mark)
                if mark_calculation == 'Exceeds':
                    messages.error(request, "Student already exits - Failed to update - Exceeds 100")
                elif mark_calculation == 'Below':
                    messages.error(request, "Student already exits - Failed to update - less tham 0")
                else:
                    messages.success(request, "Student already exits - successfully updated the mark")
                    data.mark = updated_mark
                    log_details = {
                        'user': user,
                        'action': 'Updated',
                        'student_name':data.name,
                        'student_id':student_id,
                        'details':'Student ' + str(data.subject) + ' mark is updated from ' + str(previous_mark) + ' to ' + str(updated_mark)
                    }
                    log_in_audit(log_details)
                    data.save()  

        else:
            if int(mark) > 100 or int(mark) < 0:
                messages.error(request, "Enter a valid mark between 0 and 100")
            else:
                form_data = {'name': name, 'subject': subject, 'mark': mark, 'user': user}
                form = StudentForm(form_data)
                if form.is_valid():
                    student = form.save(commit=False)
                    student.user = user
                    student.save()
                    messages.info(request, 'Student ' + str(name) + ' sucessfully added')
    return redirect("dashboard")


def update_student(request, pk):
    student = get_object_or_404(StudentDetails, id=pk)
    user_id = get_user_session(request)
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        name = request.POST['name'].capitalize()
        subject = request.POST['subject'].capitalize()
        mark = request.POST['mark']

        if int(mark) > 100 or int(mark) < 0:
            messages.error(request, "Enter a valid mark between 0 and 100")
        else:
            form_data = {'name': name, 'subject': subject, 'mark': mark, 'user': user}
            form = StudentForm(form_data, instance=student)
            if form.is_valid():
                form.save()
                log_details = {
                    'user': user,
                    'action': 'Updated',
                    'student_name':student.name,
                    'student_id':pk,
                    'details':'Student details has been updated'
                }
                log_in_audit(log_details)
                messages.success(request, "Student details sucessfully updated!")
    return redirect("dashboard")

def delete_student(request, pk):
    user_id = get_user_session(request)
    user = get_object_or_404(User, id=user_id)

    student = get_object_or_404(StudentDetails, id=pk)
    student.delete()
    log_details = {
        'user': user,
        'action': 'Deleted',
        'student_name':student.name,
        'student_id':pk,
        'details':'Student data from ' + str(student.subject) + ' has been deleted'
    }
    log_in_audit(log_details)
    messages.success(request, "Student from sucessfully deleted!")
    return  redirect("dashboard")

def logs(request):
    log_details = AuditLog.objects.all()

    context = {
        'logs' : log_details,
    }

    return render(request, 'accounts/logs.html', context)