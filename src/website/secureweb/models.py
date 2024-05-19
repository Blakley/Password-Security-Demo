from django.db import models

# ===========================
# Credentials model [Table]
# ===========================

class Credentials(models.Model):
    user_email = models.CharField(max_length = 200)
    user_password = models.CharField(max_length = 200)