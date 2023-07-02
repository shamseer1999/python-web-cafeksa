from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product
from django.core.paginator import Paginator
# Create your views here.

def adminLogin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You are successfully logged in')
            return redirect('dashboard')
        else:
            messages.warning(request,'Invalid credentials')
            return redirect('adm_login')
    return render(request,'login.html')

@login_required(login_url='/mngr/')
def index(request):
    return render(request,'dashboard.html')

@login_required(login_url='/mngr/')
def productsList(request):
    results = Product.objects.all()
    products = Paginator(results,10)
    page_number = request.GET.get("page")
    page_obj = products.get_page(page_number)
    return render(request,'products/index.html',locals())

@login_required(login_url='/mngr/')
def adminLogout(request):
    logout(request)
    return redirect('adm_login')