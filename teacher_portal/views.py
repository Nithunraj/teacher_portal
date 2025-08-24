from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    if request.session.get('user_id'):
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    return render(request,'home.html')