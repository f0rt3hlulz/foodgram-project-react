from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import PasswordResetView

from .views import UserViewSetForRequests

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSetForRequests)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        r'admin_password_reset/',
        PasswordResetView.as_view(),
        name='admin_password_reset'
    )
]
