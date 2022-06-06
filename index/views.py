from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    # form = request.POST['form']

    return render(request,"index/index.html",{})
