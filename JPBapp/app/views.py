from django.shortcuts import render,redirect
from django.http import HttpResponse
from .scripts.juliarun import juliarun
from .scripts.get_data import get_data
from .scripts.generate_video import generate
from .scripts.get_dataset import get_dataset_zip
import os
from .models import *
import datetime

# Create your views here.
def index(request):
    return redirect('/dashboard')
    # return render(request,'main/index.html')

def dashboard(request):
    data_folder_path = os.getcwd()+r'\app\scripts\data'
    files = os.listdir(data_folder_path)
    files = sorted(files, key=lambda x: int(x.split('.')[-2]))
    # Определите контекст с данными
    # context = {
    #     'data_files': files,
    #     'data_folder_path' : data_folder_path
    # }
    # file_contents=''
    # with open('app/scripts/log.txt', 'r') as file:
    #     file_contents = file.read()

    # Теперь переменная file_contents содержит весь текст из файла
    # print(file_contents)
    
    # ------------------------------------------------------------------------------

    # variable = Variable.objects.get(id=1)
    # print(Variable.objects.get(name='julia_log').description)

    # ------------------------------------------------------------------------------
    context = {
        # 'data_files': files,
        # 'data_folder_path' : data_folder_path,
        # 'file_contents' : file_contents,

        'julia_load' : Variable.objects.get(name='julia_load').description,
        'julia_log' : Variable.objects.get(name='julia_log').description,
        'julia_finish' : Variable.objects.get(name='julia_finish').description,
        'julia_start' : Variable.objects.get(name='julia_start').description,
        'generate_video_u_start' : Variable.objects.get(name = 'generate_video_u_start').description,
        'generate_video_u_name' : Variable.objects.get(name = 'generate_video_u_name').description,
        'generate_video_u_load' : Variable.objects.get(name = 'generate_video_u_load').description,
        'generate_video_u_finish' : Variable.objects.get(name = 'generate_video_u_finish').description,
        'generate_video_v_start' : Variable.objects.get(name = 'generate_video_v_start').description,
        'generate_video_v_name' : Variable.objects.get(name = 'generate_video_v_name').description,
        'generate_video_v_load' : Variable.objects.get(name = 'generate_video_v_load').description,
        'generate_video_v_finish' : Variable.objects.get(name = 'generate_video_v_finish').description,
        'download_start' : Variable.objects.get(name = 'download_start').description,
        'download_load' : Variable.objects.get(name = 'download_load').description,
        'download_finish' : Variable.objects.get(name = 'download_finish').description,

        
    }
    return render(request,'dashboard/index.html',context)

def solve(request):
    data = {
        'name': 'julia_load',
        'description': 1,
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    data = {
        'name': 'julia_start',
        'description': request.POST.get("startTime"),
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    p0sf = request.POST.get("p0sf")
    p0lf = request.POST.get("p0lf")
    cp1 = request.POST.get("cp1")
    cp2 = request.POST.get("cp2")
    cs = request.POST.get("cs")
    d0 = request.POST.get("d0")
    # f = request.POST.get("f")
    text = juliarun([p0sf, p0lf, cp1, cp2, cs, d0], r'\app\scripts\juliacode.jl')
    # Открываем файл для записи. Если файл не существует, он будет создан.
    # with open('app/scripts/log.txt', 'w') as file:
    #     # Записываем текст в файл
    #     file.write(text)
    # Файл будет автоматически закрыт после выхода из блока "with"
    
    data = {
        'name': 'julia_log',
        'description': text,
    }
    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    data = {
        'name': 'julia_finish',
        'description': datetime.datetime.now(),
    }
    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )
    data = {
        'name': 'julia_load',
        'description': 0,
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )
    return HttpResponse(text)
    # return render(request,'dashboard/index.html')
    
def datasets(request):
    data_path = request.POST.get("data_path")
    data = get_data(data_path)
    return HttpResponse(data)
    # return render(request,'dashboard/index.html')

def generate_video(request):
    
    method = request.POST.get("method")
    
    data = {
        'name': 'generate_video_{}_load'.format(method),
        'description': 1,
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )
    
    data = {
        'name': 'generate_video_{}_start'.format(method),
        'description': request.POST.get("startTime"),
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    generate_data = generate(method)

    data = {
        'name': 'generate_video_{}_finish'.format(method),
        'description': datetime.datetime.now(),
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    data = {
        'name': 'generate_video_{}_load'.format(method),
        'description': 0,
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    data = {
        'name': 'generate_video_{}_name'.format(method),
        'description': generate_data,
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )
    return HttpResponse(generate_data)
    # return render(request,'dashboard/index.html')
    
def get_dataset(request):
    data = {
        'name': 'download_load',
        'description': 1,
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )
    
    data = {
        'name': 'download_start',
        'description': request.POST.get("startTime"),
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    dataset_zip = get_dataset_zip()
    
    data = {
        'name': 'download_finish',
        'description': datetime.datetime.now(),
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )

    data = {
        'name': 'download_load',
        'description': 0,
    }

    obj, created = Variable.objects.update_or_create(
        name=data['name'],
        defaults=data
    )
    return HttpResponse(dataset_zip)
    # return render(request,'dashboard/index.html')

