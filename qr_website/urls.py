from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from .views import ProfileImageView


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    re_path(r'^upload/', ProfileImageView.as_view(), name='profile_image_upload'),
    path('excel_records/<str:pk>', views.excelRecord, name='e_record'),
    path('add_excel_file/', views.addExcelFile, name='add_excel_file'),
    path('delete_excel_file/<str:pk>', views.deleteExcelFile, name='delete_excel_file'),
    path('webcam/', views.index, name='webcam'),
    path('cam_scan/', views.webcamScanned, name='cam_scan')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)