from django.urls import path
from .views import *



urlpatterns =[
    path('addtarif/',AddTarif),
    path('addgroup/',AddGroup),
    path('addteacher/',AddTeacher),
    path('addstudent/',AddStudent),
    path('add-payment/',AddPayment)
]

