import random

def generate_verification_code():
    return str(random.randint(1000, 9999))  # 6 xonali kod

def send_sms(phone_number, message):
    """
    SMS yuborishni simulyatsiya qiladi.
    Konsolga xabar chiqariladi.
    """
    print(f"SMS {phone_number} raqamiga yuborildi: {message} , ")
    # Simulyatsiya muvaffaqiyatli bo'ldi deb hisoblaymiz
    return True
