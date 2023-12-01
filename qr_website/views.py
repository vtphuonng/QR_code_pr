import os

from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from django.template import loader
from django.views.generic import FormView, DetailView, ListView
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from .register_form import signup_form
from .forms import ProfileImageForm, AddRecordForm
from .models import ProfileImage, records
from .QR_genarator.QR_generator import *
from .quicksort_search import *
from .db.files_manager import files_generator
from .QR_genarator.test2 import *
from .quicksort_search import *
from qr_website.db.files_manager import *


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Access successfully')
            return redirect('home')
        else:
            messages.error(request, 'Login failed')
            return redirect('home')
    else:
        file = files_generator()
        file_lst = file.getFiles()

        items = []
        form_id_counter = 1

        for r in file_lst:
            file_name = r[0]
            file_path = r[1]
            file_created = r[2]
            file_last_modified = r[3]

            form = ProfileImageForm()
            items.append((file_name, file_path, file_created, file_last_modified, form, form_id_counter))
            form_id_counter += 1

        context = {'items': items, 'upload_form': ProfileImageForm()}
        return render(request, 'home.html', context)
def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, 'logout success')
    return redirect('home')


def signup_user(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            form.save()
            # Authenticated and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "login success")
            return redirect('home')
    else:
        form = signup_form()
        return render(request, 'signup.html', {'form': form})
    return render(request, 'signup.html', {'form': form})


def excelRecord(request, pk):
    if request.user.is_authenticated:
        all = records.objects.all()
        # book_record = books.objects.get(book_id=pk)
        c = to_list(all)
        print(c)
        e_records = quick_select_by_id(c, pk)
        print(e_records)
        return render(request, 'excel_records.html', {'e_records': e_records})
    else:
        messages.success(request, 'U must be logged in')
        return redirect('home')


def addExcelFile(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_excel_file.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def deleteExcelFile(request, pk):
    if request.user.is_authenticated:
        # delete_target = books.objects.get(book_id=pk)
        all = records.objects.all()
        c = to_list(all)
        delete_target = quick_select_by_id(c, pk)
        for i in delete_target:
            i.delete()
        messages.success(request, 'deleted')
        return redirect('home')
    else:
        messages.success(request, 'U must be logged in')
        return redirect('home')


# class ProfileImageView(FormView):
#     template_name = 'home.html'
#     form_class = ProfileImageForm
#
#     # def form_valid(self, form, excel_path):
#     #     profile_image = ProfileImage(
#     #         image=self.get_form_kwargs().get('files')['image'])
#     #     profile_image.save()
#     #     # time.sleep(3)
#     #     # f = files_generator()
#     #     # lst = f.getFiles()
#     #     # excel_path = f.createFiles(lst)
#     #     # print('pathpathpathpathpathpath')
#     #     print(excel_path)
#     #     m = qr_processing(excel_path)
#     #     lst = m.get_dir()
#     #     m.save_into_db(lst)
#     #     return redirect('home')
#     #
#     # def post(self, request):
#     #     # Handle POST request
#     #     posted_data = request.POST.get('some_key', 'default_value')
#     #     # Process the posted data as needed
#     #     return HttpResponse(f'Posted data: {posted_data}')

class ProfileImageView(FormView):
    template_name = 'home.html'
    form_class = ProfileImageForm

    def form_valid(self, form):
        # Assuming 'file_path' is part of the URL, extract it from the kwargs
        file_path = self.kwargs.get('file_path')

        profile_image = ProfileImage(image=form.cleaned_data['image'])
        profile_image.save()

        # Use 'file_path' in your processing logic
        m = qr_processing(file_path)
        lst = m.get_dir()
        m.save_into_db(lst)

        return redirect('home')

    def get_form_kwargs(self):
        # Pass the request.FILES to the form so it can access uploaded files
        kwargs = super().get_form_kwargs()
        kwargs['files'] = self.request.FILES
        return kwargs

def index(request):
    cap = cv2.VideoCapture(0)

    while True:
        template = loader.get_template('webcam.html')
        return HttpResponse(template.render({}, request))


def webcamScanned(requests):
    return StreamingHttpResponse(get_from_vid(), content_type='multipart/x-mixed-replace; boundary=frame')

def search_by_name_records(request, searched):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # look up record
            searched = request.POST['searched']
            folder_path = r'D:\VTP\python_workspaces\qr_pr\qr_website\db\excels'
            excel_all = os.listdir(folder_path)
            excel_path_list = []
            for obj in folder_path:
                excel_path_list.append(obj[1])
            search_results = quick_select_by_id(excel_path_list, searched)
            return render(request, 'simple_list.html', {"search_results":search_results})
        else:
            return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')