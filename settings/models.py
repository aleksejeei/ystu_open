from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class is_beta(models.Model):
    def __str__(self):
        return str(self.beta)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    beta = models.BooleanField()