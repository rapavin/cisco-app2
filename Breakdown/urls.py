from django.urls import path

from . import views

urlpatterns = [
    path('',views.Home_Page, name='Home_Page'),
    path('Cisco_Parser_Page',views.Cisco_Parser_Page, name='Cisco_Parser_Page'),
    path('Aruba_Parser_Page',views.Aruba_Parser_Page, name='Aruba_Parser_Page'),
    path('Network_Page',views.Network_Page, name='Network_Page'),
    path('upload_read',views.upload_read, name='upload_read'),
]
