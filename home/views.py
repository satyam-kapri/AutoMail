from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib import messages
from emailauto import emailauto
from emailauto import aiemail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from home import tasks
import time
from datetime import datetime
from home.models import ScheduledEmail,sender
from celery.schedules import crontab
from djangobackend.celery import app as celery_app
from django.utils import timezone
from django_celery_beat.models import PeriodicTask,CrontabSchedule
import json
from django.core import serializers

# Create your views here.
@login_required(login_url='login')
def home(request):
    try:
        if(request.user.sender.sender_mail==None):
          messages.info(request,"Please set sender's details from settings")
    except:
        messages.info(request,"Please set sender's details from settings")
    return render(request,'home.html')

def register(request):  
    if request.method=='POST':
         username=request.POST['username']
         email=request.POST['email']
         password=request.POST['password']
         my_user=User.objects.create_user(username,email,password)
         my_user.save()
         return redirect('login')
    return render(request,'register.html')

def loginpage(request):
    if(request.user.is_authenticated):
        return redirect('home')
    if request.method=='POST':
         username=request.POST['username']
         password=request.POST['password']
         user=authenticate(request,username=username,password=password)
         if user is not None:
             login(request,user)
             messages.success(request,"LoggedIn Successfully!")
             return redirect('home')
         else:
            messages.error(request,"Invalid username or password")
    return render(request,'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"Loggedout Successfully!")
    return redirect('login')

@csrf_exempt
def sendmail(request):
    if request.method=='POST':
      sender=request.user.sender.sender_mail
      app_psd=request.user.sender.app_password
      message = request.POST.get('message', None)
      excelfile=request.FILES.get('excelfile',None)
      img=request.FILES.get('img',None)
      subject=request.POST.get('subject',None)
      scheduled_datetime=request.POST.get('schedule-datetime',None)
      campaign_name=request.POST.get('campaign-name',None)
     
      scheduled_datetime= datetime.strptime(scheduled_datetime,'%Y-%m-%dT%H:%M')
      scheduled_datetime = timezone.make_aware(scheduled_datetime)
     
      scheduled_email = ScheduledEmail.objects.create(user=request.user,scheduled_time=scheduled_datetime,campaign_name=campaign_name)
      scheduled_email.csv_file.save(excelfile.name, excelfile)
      if(img):
         scheduled_email.attach_file.save(img.name, img)
      
      try:
         schedule,created=CrontabSchedule.objects.get_or_create(minute=scheduled_datetime.minute, hour=scheduled_datetime.hour, day_of_month=scheduled_datetime.day,
         month_of_year=scheduled_datetime.month)
         task=PeriodicTask.objects.create(crontab=schedule,task='home.tasks.send_emails_from_csv',name=campaign_name,args=json.dumps((scheduled_email.id,message,subject,sender,app_psd)),one_off=True)
         messages.success(request,"Scheduled Successfully!")
      except:
         print("error occured in periodic task")
         return JsonResponse({"error":"failed to schedule (check if campaign name is unique or retry)"})
    
   
    return JsonResponse({"success":"send successful"})

def promptendp(request):
    if request.method=='POST':
        key=request.user.sender.openai_api_key
        prompt=request.POST['prompt']
        gen_email=aiemail.generate_email(key,prompt)
    
    return JsonResponse({"email":gen_email})

def allcampaigns(request):
    allschedules=ScheduledEmail.objects.filter(user=request.user)
    data=serializers.serialize('json', allschedules)
    return render(request,'allcampaigns.html',{"data":data})
    
@csrf_exempt
def deletecampaign(request):
    if request.method=='DELETE':
        data = json.loads(request.body)
        cname=data.get('campaign_name')
        print(cname)
        try:
           item=ScheduledEmail.objects.get(campaign_name=cname)
           item2=PeriodicTask.objects.get(name=cname)
           item.delete()
           item2.delete()
        except:
            print("not exist")
    return HttpResponse("successfully deleted")

    
def usersettings(request):
    data=""
    obj,created=sender.objects.get_or_create(user=request.user)
    li=[obj]
    data=serializers.serialize('json', li)
    return render(request,'settings.html',{"data":data})

@csrf_exempt
def savesettings(request):
    if(request.method=='POST'):
        sendermail=request.POST.get('sender-mail',None)
        app_psd=request.POST.get('sender-app-password',None)
        openaikey=request.POST.get('openaikey',None)
        obj,created=sender.objects.get_or_create(user=request.user)
        
        if(sendermail!=""):
              obj.sender_mail=sendermail
        if(app_psd!=""):
              obj.app_password=app_psd
        if(openaikey!=""):
              obj.openai_api_key=openaikey
       
        obj.save()
        
        
    return HttpResponse('saved successfully')




























































































































