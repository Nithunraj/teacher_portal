# Django Student Management System

A simple Django-based project for managing student records with custom authentication, logging, and admin features.

---

## 🔧 Setup Instructions

1. Clone the repository  
2. Make sure you have **Python 3.8** and **Django 4.2.23** installed  
3. Run the following commands:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   
## Getting Started
1. Register a new user from the UI
2. Login using the registered user
3. Create a superuser using the terminal:
   ```bash
   python manage.py createsuperuser

## Features
1. Alert messages for login, create, update, and delete
2. Logs stored in a separate table
3. Minimal logs displayed on a dedicated screen
4. Duplicate (name + subject) entries update existing data
5. Validates marks (must be between 0–100)
6. Inline editing feature
7.Admin panel shows key data without opening records

## Security Considerations
1. Custom decorator for login-required views
2. Custom session-based login with hashed passwords
3. @never_cache used to block access to protected pages after logout

## Challenges Faced
1. Hashing and verifying custom passwords
2. Handling superuser login with custom auth
3. Building UI with basic frontend skills (minimal but usable)

## Time Taken
Approximately 15 hours (setup was quick due to prior experience)


## Pictures for the application
1. Login
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/afaf44ad-761d-4578-a70f-76fa1a3d9b31" />

2. Register
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/998e4a07-0afc-428b-8e1c-f2c82edcd67c" />

3. Dashboard
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/4ae04c16-6e47-419f-8924-a21ce40b13ec" />

4. Add student
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/3e269004-32e0-4342-b2df-aaede5a0b93d" />

5. Action Dropdown
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/f9566269-0be9-4172-9c24-ecae30f8c620" />

6. Edit Student
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/168f6409-9292-4279-b42e-691c21d7d5d1" />

7. Delete student
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/b70fcfa1-d7b2-459c-912c-b7c349c38a8f" />

8. Logs
<img width="1763" height="965" alt="image" src="https://github.com/user-attachments/assets/cdbadebe-788a-4c07-bd00-079bd9f2e851" />






