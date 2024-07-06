import csv
from django.core.mail import send_mail
from djangobackend.celery import app
from emailauto import emailauto
from home.models import ScheduledEmail
@app.task
def send_emails_from_csv(scheduledemail_id,message,subject,sender,app_psd):
      
            scheduled_email = ScheduledEmail.objects.get(id=scheduledemail_id)
            excelfile=scheduled_email.csv_file
            attach=scheduled_email.attach_file
            try:
                  emailauto.processexcel(excelfile,message,subject,attach,sender,app_psd)
                  scheduled_email.status='Completed'
                  scheduled_email.save()
      
            except Exception as e:
                  print("failure happened:",e)
                  scheduled_email.status='Failure'
                  scheduled_email.save()
      

     