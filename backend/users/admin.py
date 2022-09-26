from django import forms
from django.contrib import admin
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       UserCreationForm)

from .models import User

EMPTY = '-пусто-'


class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
    
    class Meta:
        model = User
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('__all__')
        field_classes = UserCreationForm.Meta.field_classes


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_superuser', 'is_staff', 'date_joined', 'followers_count',
    )
    empty_value_display = EMPTY
    form = CustomUserCreationForm
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    def followers_count(self, obj):
        return obj.followers.count()

    def save_model(self, request, obj, form, change):
        if obj.pk:
            if 'pbkdf2_sha256$' not in obj.password:
                obj.set_password(obj.password)
            obj.is_staff = True if obj.role == 'admin' else False
            obj.is_superuser = True if obj.role == 'admin' else False
        obj.save()
   