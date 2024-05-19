# ================================
# URL configurations for this view
# ================================

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]

