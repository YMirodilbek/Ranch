from django.db import models
import re
import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from PIL import Image
# from django.contrib.sites.models import Site

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak."
    )   
    phone_number = models.CharField(max_length=13, validators=[phone_regex],unique=True)
    referral_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Telefon raqamni formatlash
        if self.phone_number:
            cleaned_number = ''.join(filter(str.isdigit, self.phone_number))
            if cleaned_number.startswith('998') and len(cleaned_number) == 12:
                self.phone_number = f"+{cleaned_number}"
            elif not cleaned_number.startswith('+998'):
                raise ValueError("Telefon raqam noto'g'ri formatda.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} "

    def get_referral_link(self):
        
        return f"http://localhost:8000/users/invite/{self.referral_code}/"





class Category(models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name
    
class Books(models.Model):
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    text = models.TextField()
    kitob = models.FileField(upload_to='media/')
    total_pages = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.width > 292 or img.height > 443:  # Maksimal o'lcham
                img.thumbnail((292, 443))  # O'lchamni kichraytirish
                img.save(self.image.path)  # O'zgartirilgan rasmlarni saqlash
        super(Books, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    


class BookReading(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)  # O'qish tugatilganini belgilash
    date_completed = models.DateTimeField(null=True, blank=True)
    current_page = models.IntegerField(default=1)
    last_read_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
class Aloqa(models.Model):
    name = models.CharField(max_length=90)
    phone = models.CharField(max_length=20)
    mavzu = models.CharField(max_length=200)
    text = models.TextField()
   

    def __str__(self):
        return self.name