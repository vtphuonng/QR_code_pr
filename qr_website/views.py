import pandas as pd

from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse, JsonResponse
from django.template import loader
from django.views.generic import FormView, DetailView, ListView
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST


from .register_form import signup_form
from .forms import ProfileImageForm, AddRecordForm
from .models import ProfileImage, records
from django.forms.models import model_to_dict
from .QR_genarator.QR_generator import *
from .quicksort_search import *
from .db.files_manager import files_generator
from .QR_genarator.test2 import *
from .quicksort_search import *
from qr_website.db.files_manager import *


# kêt nối với giao diện home tr
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


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd


# views.py

def excelRecord(request, pk):
    if request.user.is_authenticated:
        try:
            # Read the Excel file to get sheet names
            xls = pd.ExcelFile(pk)
            sheet_names = xls.sheet_names
            xls.close()

            # Get the selected sheet from the form submission
            selected_sheet = request.GET.get('selected_sheet', '')
            if not selected_sheet:
                selected_sheet = sheet_names[0]

            # Read data from the selected sheet
            df = pd.read_excel(pk, selected_sheet)
            records_list = df.values.tolist()

            items = [(r[1], r[2]) for r in records_list if r[1] and r[2]]

            if 'recycleBin' in str(pk):
                tail = Path(pk).name
                context = {'sheet_names': sheet_names, 'selected_sheet': selected_sheet, 'items': items,
                           'your_excel_file_id': pk, 'tail': tail}
            else:
                context = {'sheet_names': sheet_names, 'selected_sheet': selected_sheet, 'items': items,
                           'your_excel_file_id': pk}
        except Exception as e:
            messages.error(request, f"Error reading Excel file: {e}")
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in')
        return redirect('home')

    return render(request, 'excel_records.html', context)

@require_POST
def addExcelFile(request):
    if request.user.is_authenticated:
        input_text = request.POST.get('customInput', '')
        print('----------------',input_text)
        if input_text:
            fm = files_generator()
            create_file = fm.createFiles(input_text)
            if create_file[0] == True:
                messages.success(request, "File Existed")
                return JsonResponse({'message': 'File Existed', 'input_text': input_text})
            else:
                messages.success(request, "File Created")
                return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def deleteExcelFile(request, deleted_file):
    if request.user.is_authenticated:
        fm = files_generator()
        delete_mess = fm.deleteFile(deleted_file)
        messages.success(request, delete_mess)
        return redirect('home')
    else:
        messages.success(request, 'U must be logged in')
        return redirect('home')

def recycleBin(request):
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
        file = recycleManage()
        file_lst = file.getDummy()

        items = []
        form_id_counter = 1

        for r in file_lst:
            file_name = r[0]
            file_path = r[1]
            create_time = r[2]
            deleted_time = r[3]
            items.append((file_name, file_path, create_time, deleted_time, form_id_counter))
            form_id_counter += 1

        context = {'items': items}
        return render(request, 'recycleBin.html', context)

def removeFile(request, rm_file):
    if request.user.is_authenticated:
        print('F4', rm_file)
        fm = recycleManage()
        delete_mess = fm.removeFile(rm_file)
        messages.success(request, delete_mess)
        return redirect('home')
    else:
        messages.success(request, 'U must be logged in')
        return redirect('home')

def recoveryFile(request, recovey_file):
    if request.user.is_authenticated:
        fm = files_generator()
        recovery_mess = fm.recoveryFile(recovey_file)
        messages.success(request, recovery_mess)
        return redirect('bin_list')
    else:
        messages.success(request, 'U must be logged in')
        return redirect('bin_list')
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
        file_path = self.kwargs.get('file_path')

        profile_image = ProfileImage(image=form.cleaned_data['image'])
        profile_image.save()

        # Use 'file_path' in your processing logic
        m = qr_processing(file_path)
        lst = m.get_dir()
        m.save_into_db(lst)
        messages.success(self.request, 'Upload successful')
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


def webcamScanned(requests, pk):
    return StreamingHttpResponse(get_from_vid(pk), content_type='multipart/x-mixed-replace; boundary=frame')


def search_by_name_records(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')

        rm = recycleManage()
        lst = rm.getDummy()
        print(lst)
        items = []
        cache1 = []
        cache2 = []
        form_id_counter = 0
        exits_counter = 0
        no_exits_counter = 0
        cache3 = []
        for r in lst:
            if query and query in r[0]:
                print(r[0])
                print('SEARCH IN')
                file_name = r[0]
                file_path = r[1]
                create_time = r[2]
                deleted_time = r[3]
                cache1.append({
                    'file_name': file_name,
                    'file_path': file_path,
                    'create_time': create_time,
                    'deleted_time': deleted_time,
                    'form_id_counter': form_id_counter
                })
                form_id_counter += 1
                exits_counter += 1
            elif query and query not in r[0]:
                cache3.append({
                    'file_name': 'Not Found',
                    'file_path': 'Not Found',
                    'create_time': 'Not Found',
                    'deleted_time': 'Not Found',
                })
            else:
                print('SEARCH IN')
                file_name = r[0]
                file_path = r[1]
                create_time = r[2]
                deleted_time = r[3]
                cache2.append({
                    'file_name': file_name,
                    'file_path': file_path,
                    'create_time': create_time,
                    'deleted_time': deleted_time,
                    'form_id_counter': form_id_counter
                })
                form_id_counter += 1

        if exits_counter != 0:
            print('FP', query)
            print('FP2', cache1)
            items = cache1
            return JsonResponse({'items': items})
        elif no_exits_counter != 0:
            items = cache3
            return JsonResponse({'items': items})
        print('FP', query)
        print('FP2', cache2)
        items = cache2
        return JsonResponse({'items': items})

    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def searchHome(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')

        fm = files_generator()
        lst = fm.getFiles()

        items = []
        cache1 = []
        cache2 = []
        cache3 = []
        form_id_counter = 0
        exits_counter = 0
        no_exists_counter = 0

        for r in lst:
            if query and query in r[0]:
                file_name = r[0]
                file_path = r[1]
                file_created = r[2]
                file_last_modified = r[3]
                form = ProfileImageForm()
                form_data = {field_name: form[field_name].value() for field_name in form.fields}
                cache1.append({
                    'file_name': file_name,
                    'file_path': file_path,
                    'create_time': file_created,
                    'file_last_modified': file_last_modified,
                    'form': form_data,
                    'form_id_counter': form_id_counter
                })
                form_id_counter += 1
                exits_counter += 1
            elif query and query not in r[0]:
                no_exists_counter += 1
                cache3.append({
                    'file_name': 'Not Found',
                    'file_path': 'Not Found',
                    'create_time': 'Not Found',
                    'file_last_modified': 'Not Found',
                })
            else:
                file_name = r[0]
                file_path = r[1]
                file_created = r[2]
                file_last_modified = r[3]
                form = ProfileImageForm()
                form_data = {field_name: form[field_name].value() for field_name in form.fields}
                cache2.append({
                    'file_name': file_name,
                    'file_path': file_path,
                    'create_time': file_created,
                    'file_last_modified': file_last_modified,
                    'form': form_data,
                    'form_id_counter': form_id_counter
                })
                form_id_counter += 1

        if exits_counter != 0:
            items = cache1
            return JsonResponse({'items': items})
        elif no_exists_counter != 0:
            items = cache3
            return JsonResponse({'items': items})
        items = cache2
        return JsonResponse({'items': items})

    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
    
# views.py
from django.http import FileResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import MyModel
import os

class ExcelFileDownloadView(View):
    def get(self, request, pk):
        # Retrieve the corresponding MyModel instance based on the file path
        my_model_instance = get_object_or_404(MyModel, file_path=pk)

        # Construct the full file path using the separate folder
        file_path = os.path.join('path_to_your_separate_folder', my_model_instance.file_path)

        # Ensure the file exists before attempting to open it
        if os.path.exists(file_path):
            with open(file_path, 'rb') as excel_file:
                response = FileResponse(excel_file)
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            # Handle the case where the file does not exist
            return HttpResponse("File not found", status=404)

