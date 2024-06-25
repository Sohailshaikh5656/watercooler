from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


def send_forget_password_mail_to_agency(email, order_id, quantity,price,supplier_phone,total_price,token):
    domain = settings.DOMAIN    
    subject = 'Approval for Order /'
    message = f'Hi, User ,\n Your Order_ID  is {order_id},\n ' \
        f'Order Quantity : {quantity},\n ' \
        f'Price Per Peice : {price},\n ' \
        f'Total Cost : {total_price},\n ' \
        f'For any Query Contact to this Phone Number : {supplier_phone},\n ' \
        f'Click Here to Download the Copy of receipt http://{settings.DOMAIN}suppliers/Receipt?token={token}\n '\
        f'Thanks and regards'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True