from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import UserForm, StudentForm
from .models import User, StudentDetails, AuditLog
from django.contrib import messages, auth
from .utils import verify_password, get_user_session, calculate_new_marks, hash_password

# Create your views here.
def log_in_audit(user,action,student_id):
    AuditLog.objects.create(
                user=user,
                action=action,
                student_id=student_id,
            )
    return "Logged Successfully"

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
            return redirect('/admin/')
            
        
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
        name = request.POST['name'].capitalize()
        subject = request.POST['subject'].capitalize()
        mark = request.POST['mark']

        student = StudentDetails.objects.filter(name=name, subject=subject)
        if student.exists():
            for data in student:
                student_id = data.id
                mark_calculation, updated_mark = calculate_new_marks(mark, data.mark)
                if mark_calculation == 'Exceeds':
                    messages.error(request, "Student already exits - Failed to update - Exceeds 100")
                elif mark_calculation == 'Below':
                    messages.error(request, "Student already exits - Failed to update - less tham 0")
                else:
                    messages.success(request, "Student already exits - successfully updated the mark")
                    data.mark = updated_mark
                    log_in_audit(user, 'updated', student_id)
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
                log_in_audit(user, 'updated', pk)
                messages.success(request, "Student details sucessfully updated!")
    return redirect("dashboard")

def delete_student(request, pk):
    user_id = get_user_session(request)
    user = get_object_or_404(User, id=user_id)

    student = get_object_or_404(StudentDetails, id=pk)
    student.delete()
    log_in_audit(user, 'Deleted', pk)
    return  redirect("dashboard")