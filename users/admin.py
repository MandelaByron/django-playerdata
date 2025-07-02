from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', "first_name", "last_name", "is_staff", "username","public_id"]
    
    search_fields = ['email', "fist_name", "last_name"]
    
    fieldsets = (
        (
           (None, {"fields":("password",)})
           
        ),
        
        (
            ("Personal Info", {"fields":('first_name', 'last_name', 'email','avatar')})
        ),

        (
            ("Permissions", {"fields":('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')})
        
        ),
        
        (
            ("Important Dates", {"fields":("last_login", )})
        )
    )
    
    add_fieldsets =(
        
        (None, {
            'classes': ('wide',),
            'fields': ("first_name","last_name",'email', 'password1', 'password2'),
        }),
        
    )
    
    
    ordering = ['email']