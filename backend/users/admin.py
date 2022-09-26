from django import forms
from django.contrib import admin
django.contrib.auth.admin.UserAdmin

from .models import User

EMPTY = '-пусто-'


class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(admin.UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_superuser', 'is_staff', 'date_joined', 'followers_count',
    )
    empty_value_display = EMPTY
    form = UserAdminForm
    search_fields = ('email', 'username')
    readonly_fields = ('date_started')

    def followers_count(self, obj):
        return obj.followers.count()
