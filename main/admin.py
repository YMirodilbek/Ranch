from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        # Telefon raqamni tozalash va formatlash
        cleaned_number = ''.join(filter(str.isdigit, obj.phone_number))
        if cleaned_number.startswith('998') and len(cleaned_number) == 12:
            obj.phone_number = f"+{cleaned_number}"
        super().save_model(request, obj, form, change)
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'referral_code', 'referred_by','earnings','is_paid']
    list_filter = ('is_paid', 'is_staff')
    list_editable = ['earnings','is_paid',]

admin.site.register(CustomUser, CustomUserAdmin)



class BookAdmin(admin.ModelAdmin):
    # Ko'rinadigan ustunlar
    list_display = ('title', 'author', 'date_created')

    # Qidiruv maydoni
    search_fields = ('title', 'author', 'category')
 
    # Filtrlash imkoniyati
    list_filter = ('category', 'author')


admin.site.register(Books, BookAdmin)
admin.site.register(Category)
admin.site.register(Aloqa)
