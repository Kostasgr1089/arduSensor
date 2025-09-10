
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('arduSensorAPI.urls')), 
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', RedirectView.as_view(url='/api/display-data/', permanent=False), name='home'),
    
]
