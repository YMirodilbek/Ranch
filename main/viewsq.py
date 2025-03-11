from django.shortcuts import render,redirect
from .forms1 import *
from django.core.exceptions import ValidationError
from django.contrib import messages


def AddTarif(request):
    if request.method == 'POST':
        forms = TarifForm(request.POST)

        if forms.is_valid():
            forms.save()
            messages.success(request,'Tarif muvaffaqiyatli Yaratildi !!')
            return redirect('/addtarif/')
        else:
            messages.error(request,"Tarif yaratilishda Xatolik Mavjud !! ")
    else:
        forms = TarifForm()


    
    return render(request,'tarif.html',{'forms',forms})


def AddGroup(request):
    if request.method == "POST":
        forms = GroupForm(request.POST)

        if forms.is_valid():
            forms.save()
            messages.success(request , "Grupa Yaratildi !!")
            return redirect('/addgroup/')
        else:
            messages.error(request,"Grux Yaratishda Xatolik mavjud !!")
    else:
        forsm = GroupForm()
    context={
        "forms":forms
    }
    return render(request,'group.html',context)



    