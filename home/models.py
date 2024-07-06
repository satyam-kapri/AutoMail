from django.db import models
from django.contrib.auth.models import User

class sender(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    sender_mail=models.CharField(max_length=50,null=True,blank=True)
    app_password=models.CharField(max_length=50,null=True,blank=True)
    openai_api_key=models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return str(self.user)

class ScheduledEmail(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    campaign_name=models.CharField(max_length=200,default='unique value')
    csv_file = models.FileField(upload_to='uploads/',blank='true')
    attach_file=models.FileField(upload_to='uploads/',blank='true')
    scheduled_time = models.DateTimeField()
    status=models.CharField(max_length=20,default='Scheduled')
    def __str__(self):
        return str(self.campaign_name)
