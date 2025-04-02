from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def send_verification_email(request, user, mail_subject, email_template):
    

    # Create verification URL
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_mail = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_mail])
    mail.send()




def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role ==2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None or user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
