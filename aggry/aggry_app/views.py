from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
import os
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Jobs
from .forms import JobSearchForm
from django.core.paginator import Paginator

# Create your views here.
 
   
def frontpage(request):
    if request.method == "POST":
        form = JobSearchForm(request.POST)
        if form.is_valid():            
            # リダイレクト先のパスを取得する
            redirect_url = reverse('aggry_app:home')
            # 職種と勤務地のパラメータを作成
            parameters = urlencode({'job': form.cleaned_data['job'], 'location': form.cleaned_data['location']})
            # URLにパラメータを付与する
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
    else:
        form = JobSearchForm()       
    return render(request, "aggry_app/frontpage.html", {"form": form})


def home(request):
    jobs = Jobs.objects.filter(job=request.GET.get('job'), mod_location=request.GET.get('location')).all()
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'aggry_app/home.html', context = {
        "jobs": jobs,
        "page_obj": page_obj,
        "request": request,
        "job": request.GET.get('job'),
        "location": request.GET.get('location'),
    })

def job_detail(request, id):
    job = Jobs.objects.get(id=id)
    return render(request, "aggry_app/job_detail.html", context = {
        "job": job
        })