from django.contrib import admin
from home.models import sender
from home.models import ScheduledEmail
# Register your models here
admin.site.register(sender)
admin.site.register(ScheduledEmail)