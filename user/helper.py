from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


def send_forget_password_mail_to_agency(email, branchname, ownername,token):
    domain = settings.DOMAIN    
    subject = 'Your Change Password'
    message = f'Hi, {ownername},\n Your Branch Name is {branchname},\n ' \
           f'Click here to change your password: http://{settings.DOMAIN}/user/changePassword?token={token}\n ' \
           f'Thanks and regards'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True