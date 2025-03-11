from django.shortcuts import render,redirect
from .models import *
from .forms import *
from decimal import Decimal
from django.contrib.auth import login, authenticate,logout

from django.contrib.auth.decorators import login_required
from .utils import generate_verification_code,send_sms
from django.contrib import messages


from django.shortcuts import get_object_or_404
from django.utils.timezone import now

#Authenticates

def Register(request, referral_code=None):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Parolni xavfsiz saqlash

            if referral_code:
                # Referral kodi mavjud bo'lsa, referal egasini topish
                try:
                    referring_user = CustomUser.objects.get(referral_code=referral_code)
                    user.referred_by = referring_user  # Yangi foydalanuvchini referal egasiga o'rnatish

                    # Referal egasiga bonus qo‘shish
                    referring_user.earnings += Decimal('10.00') 
                     # Masalan, 10.00 pul qo‘shish
                    print(referring_user.earnings)
                    print(referring_user)
                    referring_user.save()
                except CustomUser.DoesNotExist:
                    form.add_error(None, "Noto'g'ri referral kodi.")  # Referral kod noto'g'ri bo'lsa

            user.save()  # Foydalanuvchini saqlash
            login(request, user)  # Yangi foydalanuvchini tizimga kiriting
            return redirect('/')  # Bosh sahifaga yuborish
    else:
        form = CustomUserForm()

    return render(request, 'registration/SignUp.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect('/home/')  # Home page
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'registration/Login.html', {'form': form})
        
def Logout(request):
    logout(request)
    return redirect('/')


from django.contrib.auth import get_user_model

User = get_user_model()


def request_password_reset_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            

            try:
                # Telefon raqamga mos foydalanuvchini topish
                user = User.objects.get(phone_number=phone_number)

                verification_code = generate_verification_code()
                
                # Sessiyaga tasdiqlash kodi va foydalanuvchi ID-ni saqlash
                request.session['verification_code'] = verification_code
                request.session['reset_user_id'] = user.id
               

                # SMS yuborish
                message = f"Parolni tiklash uchun tasdiqlash kodi: {verification_code}"
                if send_sms(phone_number, message):
                    
                    messages.success(request, f"Tasdiqlash kodi yuborildi. Iltimos, kodingizni kiriting. Username: {user.username}")
                    return redirect('/verify-code/')
                else:
                    messages.error(request, "Tasdiqlash kodini yuborishda muammo yuz berdi.")
            except User.DoesNotExist:
                messages.error(request, "Telefon raqami tizimda topilmadi.")
    else:
        form = PhoneNumberForm()
    return render(request, 'password_reset/request_reset.html', {'form': form})


def verify_code_view(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('verification_code'):
                messages.success(request, "Tasdiqlash kodi to'g'ri. Endi yangi parol o'rnatishingiz mumkin.")
                return redirect('/reset-password/')
            else:
                messages.error(request, "Tasdiqlash kodi noto'g'ri.")
    else:
        form = VerificationCodeForm()
    return render(request, 'password_reset/verify_code.html', {'form': form})



from django.contrib.auth.hashers import make_password

def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('reset_user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                user.password = make_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, "Parolingiz tiklandi. Endi tizimga kiring.")
                return redirect('/login/')
            else:
                messages.error(request, "Foydalanuvchi topilmadi. Jarayonni qayta boshlang.")
    else:
        form = ResetPasswordForm()
    return render(request, 'password_reset/reset_password.html', {'form': form})

    
####Homes

def Index(request):
    return render(request,'index.html')


def Main(request):
    return render(request,'Krish2.html')


def Home(request):
    category_id = request.GET.get('category') 


    category = Category.objects.all()

    if category_id:
        books = Books.objects.filter(category__id=category_id)
    else:
        books = Books.objects.all()
    
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Books.objects.filter(title__icontains=query)|Books.objects.filter(author__icontains=query)  # Qidiruv: sarlavha bo'yicha
    else:
        form = SearchForm()
    context={
        'book':books,
        "category":category,
        'result':results,
        'query':query,
        'form':form

    }
    return render(request,'home.html',context)



from django.views.generic import DetailView
class BookDetail(DetailView):
    model = Books
    template_name = 'BookPg.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kitobning tavsifi
        text = context['book'].text

        # Matnni bo'laklarga ajratish
        words = text.split()  # So'zlarni ajratish
        chunks = [words[i:i+14] for i in range(0, len(words), 14)]  # Har 4 so'zni bo'lib ajratish
        context['chunks'] = chunks  # Bu bo'laklarni konteynerga qo'shamiz
        
        return context
    def post(self, request, *args, **kwargs):
        # Kitob ob'ektini oling
        book = self.get_object()
        # 'lock' sahifasiga ID bilan o'tkazamiz
        return redirect('/ready-reading/', pk=book.pk)
    

@login_required
def complete_book(request, book_id):
    # Kitobni olish (yoki tekshirish)
    book = get_object_or_404(Books, id=book_id)
    
    # Foydalanuvchi
    user = request.user
    
    # Foydalanuvchining daromadiga 15.00 so'm qo'shish
    user.earnings += Decimal('15.00')
    user.save()

    # Foydalanuvchiga muvaffaqiyatli xabar ko'rsatish
    messages.success(request, f"{book.title} kitobini o'qishni tugatdingiz. 15 so'm qo'shildi.")
    
    # Kitob sahifasiga qaytarish
    return redirect('/home/', pk=book.id)

def Reading(request, pk):
    # Kitobni ID orqali oling
    book = Books.objects.get(pk=pk)
    context={
        'book':book
    }
    return render(request,'reading.html',context)



def ReadyBook(request):
    return render(request,'reading.html')

def Hamyon(request):
    return render(request,'hamyon.html')


def Contact(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        mavzu = request.POST['mavzu']
        text = request.POST['text']
        Aloqa.objects.create(name=name,phone=phone,mavzu=mavzu,text=text)
        return redirect('/contact/')
    return render(request,'yordam.html')

def Referal(request):
    return render(request,'referal.html')
from datetime import timedelta


def read_book(request, pk):
    book = Books.objects.get(id=pk)
    progress, created = BookReading.objects.get_or_create(user=request.user, book=book)

    # Vaqtni tekshirish
    min_time_required = progress.last_read_time + timedelta(seconds=10)  # 10 soniya
    if now() < min_time_required:
        time_remaining = (min_time_required - now()).seconds
        return render(request, 'book_reader.html', {
            'book': book,
            'progress': progress,
            'error': f"Sahifani o'qish uchun yana {time_remaining} soniya kuting.",
        })

    # Keyingi sahifaga o'tish
    if request.method == "POST" and 'next_page' in request.POST:
        if progress.current_page < book.total_pages:
            progress.current_page += 1
            progress.save()
        return redirect('/read_book/', pk   =pk)

    return render(request, 'book_reader.html', {'book': book, 'progress': progress})