from django.shortcuts import render
from django.http import HttpResponse
from .scripts.juliarun import juliarun
from .scripts.get_data import get_data
from .scripts.generate_video import generate
from .scripts.get_dataset import get_dataset_zip
import os

# Create your views here.
def index(request):
    return render(request,'main/index.html')

def dashboard(request):
    data_folder_path = os.getcwd()+r'\app\scripts\data'
    files = os.listdir(data_folder_path)
    files = sorted(files, key=lambda x: int(x.split('.')[-2]))
    # Определите контекст с данными
    context = {
        'data_files': files,
        'data_folder_path' : data_folder_path
    }
    return render(request,'dashboard/index.html',context)

def solve(request):
    p0sf = request.POST.get("p0sf")
    p0lf = request.POST.get("p0lf")
    cp1 = request.POST.get("cp1")
    cp2 = request.POST.get("cp2")
    cs = request.POST.get("cs")
    d0 = request.POST.get("d0")
    f = request.POST.get("f")
    text = juliarun([p0sf, p0lf, cp1, cp2, cs, d0, f], r'\app\scripts\juliacode.jl')
    return HttpResponse(text)
    # return render(request,'dashboard/index.html')
    
def datasets(request):
    data_path = request.POST.get("data_path")
    data = get_data(data_path)
    return HttpResponse(data)
    # return render(request,'dashboard/index.html')

def generate_video(request):
    method = request.POST.get("method")
    data = generate(method)
    return HttpResponse(data)
    # return render(request,'dashboard/index.html')
    
def get_dataset(request):
    data = get_dataset_zip()
    return HttpResponse(data)
    # return render(request,'dashboard/index.html')

