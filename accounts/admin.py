from django.contrib import admin
from .models import User, StudentDetails, AuditLog
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# To make passwords not editable from the admin panel
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email','is_staff', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name','subject','user','modified_date',)

class AdminLogPanel(admin.ModelAdmin):
    list_display = ('user','student_id','action','timestamp',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentDetails, FoodItemAdmin)
admin.site.register(AuditLog, AdminLogPanel)