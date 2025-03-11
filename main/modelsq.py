from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    LAVOZIM=(
        ("Direktor","Direktor"),
        ("Admin","Admin"),
        ("Teacher","Teacher")
    )

    phone = models.CharField(max_length=13)
    lavozim = models.CharField(max_length=20,choices=LAVOZIM,default="Teacher")
    birth_year = models.DateField(null = True,blank = True)

    def __str__(self):
        return self.username
    
class Tarif(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    

class Group(models.Model):
    name = models.CharField(max_length=90)
    teacher = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount = models.IntegerField()
    start_date = models.DateField()

    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=90)
    birth_year = models.DateField()
    phone = models.CharField(max_length=13)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Tolov(models.Model):
    amount = models.FloatField(default=0.0)
    date = models.DateField()
    student_name = models.ForeignKey(Student , on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)


    def __str__(self):
        return self.student_name

    