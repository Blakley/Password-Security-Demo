from django.db import models

# ===========================
# Credentials model [Table]
# ===========================

class Credentials(models.Model):
    user_email = models.CharField(max_length = 200)
    user_password = models.CharField(max_length = 200)
    
    # string represention for object
    def __str__(self):
        # used when entering command 'Credentials.objects.all()'
        return self.user_email + " : " + self.user_password
        