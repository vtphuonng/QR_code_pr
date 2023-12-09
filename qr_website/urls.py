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
    path('profile_image_upload/<str:file_path>/', ProfileImageView.as_view(), name='profile_image_upload'),
    path('excel_records/<str:pk>/', views.excelRecord, name='e_record'),
    path('add_excel_file/', views.addExcelFile, name='add_excel_file'),
    path('delete_excel_file/<str:deleted_file>', views.deleteExcelFile, name='delete_excel_file'),
    path('remove/<str:rm_file>', views.removeFile, name='rm_file'),
    path('webcam/', views.index, name='webcam'),
    path('cam_scan/<str:pk>/', views.webcamScanned, name='cam_scan'),
    path('search_results', views.search_by_name_records, name='search_results'),
    path('bin_list', views.recycleBin, name='bin_list'),
    path('recovery<str:recovey_file>', views.recoveryFile, name='recovery_path'),
    path('search/', views.search_by_name_records, name='search_results'),
    path('search_home/', views.searchHome, name='search_home'),
    path('download/<path:pk>/', views.ExcelFileDownloadView.as_view(), name='file_download'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)