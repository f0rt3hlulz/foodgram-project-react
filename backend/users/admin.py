from django import forms
from django.contrib import admin

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
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_superuser', 'is_staff', 'date_joined', 'followers_count',
    )
    readonly_fields = ('date_joined',)
    empty_value_display = EMPTY
    form = UserAdminForm
    fields = ('username', 'email', 'first_name', 'last_name',
        'is_superuser', 'is_staff', 'followers_count',)
    search_fields = ('email', 'username')

    def followers_count(self, obj):
        return obj.followers.count()
