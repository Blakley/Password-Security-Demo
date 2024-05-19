from django.contrib import admin
from .models import Credentials

# =====================
# Configure admin page
# =====================

# register Credentials Table
admin.site.register(Credentials)

