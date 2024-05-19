# ================================
# URL configurations for this view
# ================================

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("playground/", views.playground, name="playground"),
    path('login/', views.login, name='login'),
    path("error/", views.error, name="error"),
]

