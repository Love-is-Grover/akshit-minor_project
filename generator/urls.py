from . import views
from django.urls import path

urlpatterns = [
    path("",views.home,name = "home"),
    path("generator",views.generator , name = "generator"),
    path("audio",views.audio , name = "audio"),
    path("register", views.register, name = "register"),
    path("login", views.login, name = "login"),
    path("logout", views.logout, name = "logout"),
    path("feedback", views.feedback, name = "feedback"),
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
]