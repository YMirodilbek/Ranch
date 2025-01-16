from django.db import models
from main.models import *
from django.contrib.auth.models import User
# Create your models here.

class Transactions(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10 , default=99000,decimal_places=2)

    def __str__(self):
        return self.user.first_name