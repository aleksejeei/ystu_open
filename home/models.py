from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class session_data(models.Model):
    def __str__(self):
        return self.session_key

    session_key = models.CharField(max_length=100, primary_key=True)
    user_agent = models.CharField(max_length=100)
    data_first_auth = models.DateTimeField(auto_now=True)


class ystu_account(models.Model):
    def __str__(self):
        return self.full_name
    #username_django = models.CharField(max_length=100, unique=True, primary_key=True)
    username_django = models.OneToOneField(User, to_field='username', unique=True, primary_key=True, on_delete=models.CASCADE)
    login = models.CharField(max_length=100, unique=True)
    #login = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=False)
    full_name = models.CharField(max_length=200, null=False)
    group = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=500)
    ystu_email = models.CharField(max_length=100, null=False)
    private_email = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    numlib = models.CharField(max_length=20)
    faculty = models.CharField(max_length=200)
    direction_name = models.CharField(max_length=100)
    direction_code = models.CharField(max_length=50)
    avatar_image = models.ImageField(upload_to='avatars/', default='img.png')