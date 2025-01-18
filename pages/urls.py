from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainpage),
    path('company/', views.company),
    path('support/', views.support),
    path('support/submit/', views.submit_inquiry, name='submit_inquiry'),
]
