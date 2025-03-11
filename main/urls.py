from django.urls import path
from .views import *

urlpatterns = [
#authentication
    path('signup/',Register),
    path('signup/<uuid:referral_code>/',Register),
    path('login/',login_view),
    path('logout/',Logout),

    
    path('send-code/', request_password_reset_view, name='send_code'),
    path('verify-code/', verify_code_view, name='verify_code'),
    path('reset-password/', reset_password_view, name='reset_password'),

#Html
    path('',Index),
    path('main/',Main),
    path('home/',Home),
    path('hamyon/',Hamyon),
    path('contact/',Contact),
    path('referal/',Referal),


    #Books

    path('detailbook/<int:pk>/',BookDetail.as_view()),
    path('book/<int:pk>/',read_book),
    path('<int:pk>/ready-reading/',Reading),
    path('ready-book/',ReadyBook),
    path('book/<int:book_id>/complete/',complete_book, name='complete_book'),


    



]