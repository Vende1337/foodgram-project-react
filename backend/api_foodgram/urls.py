from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from api.views import CustomAuthToken

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/token/login/',CustomAuthToken.as_view() )
]
