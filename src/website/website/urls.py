# ===================
# URL configurations
# ===================

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('secureweb/', include("secureweb.urls")),
    path('admin/', admin.site.urls),
]
