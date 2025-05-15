from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/credentials/', views.login_with_credentials, name='login_with_credentials'),
    path('login/face/', views.login_with_face, name='login_with_face'),
    path('logout/', views.logout_view, name='logout'),
]
