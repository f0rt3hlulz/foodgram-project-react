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
    password = forms.PasswordInput()

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
   