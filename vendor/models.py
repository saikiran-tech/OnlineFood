from django.db import models
from foodapp.models import User, UserProfile
from foodapp.utils import send_notification_mail
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            original = Vendor.objects.get(pk=self.pk)
            if original.is_approved != self.is_approved:
                email_template = 'accounts/emails/admin_approval_email.html'
                context = {
                        'user': self.user,
                        'is_appoved': self.is_approved
                    }
                if original.is_approved == True:
                    mail_subject = "Congrats! Your restaurent has been approved."
                    
                    send_notification_mail(mail_subject, email_template, context) #send notification to user

                else:
                    mail_subject = "Sorry! Your restaurent is not eligible for listing."
                    send_notification_mail(mail_subject, email_template, context)

        return super(Vendor, self).save(*args, **kwargs)
