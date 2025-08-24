from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
import hashlib
import os

def hash_password(password: str, salt: str = None):
    if not salt:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${pwd_hash}"

def verify_password(stored_password: str, provided_password: str):
    try:
        salt, pwd_hash = stored_password.split('$')
        return hash_password(provided_password, salt) == stored_password
    except ValueError:
        return False
    
def get_user_session(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.info(request, 'Get user session failed, Kindly login again')
        return redirect('login')
    return user_id

def calculate_new_marks(existing, new):
    total_mark = int(existing) + int(new)
    if total_mark > 100:
        return 'Exceeds', total_mark
    elif total_mark < 0:
        return 'Below', total_mark
    else:
        return True, total_mark