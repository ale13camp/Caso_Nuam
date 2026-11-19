from django.contrib.auth import views as auth_views
from django.urls import path

from core import views
from core.admin import site

urlpatterns = [
    path('admin/', site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('calificaciones/', views.qualifications, name='qualifications'),
    path('calificaciones/<int:pk>/', views.qualification_detail, name='qualification_detail'),
    path('ingreso/', views.entry, name='entry'),
    path('carga/', views.upload, name='upload'),
    path('historial/', views.history, name='history'),
]
