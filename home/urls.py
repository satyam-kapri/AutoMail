from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path("",views.loginpage,name='login'),
    path("home",views.home,name='home'),
    path('register',views.register,name='register'),
    path('logout',views.handlelogout,name='logout'),
    path("sendmail",views.sendmail),
    path("promptendp",views.promptendp),
    path("allcampaigns",views.allcampaigns,name='allcampaigns'),
    path("deletecampaign",views.deletecampaign),
    path("usersettings",views.usersettings),
    path("savesettings",views.savesettings),
]