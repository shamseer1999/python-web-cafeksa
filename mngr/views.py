from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .forms import ProductForm
# Create your views here.

User = get_user_model() 

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
    productCount = Product.objects.count()
    userCount = User.objects.count()
    
    context = {
        'products' : productCount,
        'users' : userCount
    }
    # print("fgd",productCount)
    return render(request,'dashboard.html',context)

@login_required(login_url='/mngr/')
def productsList(request):
    results = Product.objects.order_by('-id').all()
    products = Paginator(results,10)
    page_number = request.GET.get("page")
    page_obj = products.get_page(page_number)
    return render(request,'products/index.html',locals())

@login_required(login_url='/mngr/')
def addProduct(request):
    if request.method =='POST':
        form = ProductForm(request.POST)
        print("ff",form.errors)
        if form.is_valid():
            form.save()
            messages.success(request,'Your prodect added successfully')
            return redirect('product_list')
    else:
        form = ProductForm()    
      
    context = {
        'form' : form,
        'errors' : form.errors
    }
    return render(request,'products/add.html',context)

@login_required(login_url='/mngr/')
def usersList(request):
    
    users = User.objects.order_by('-id').all()
    results = Paginator(users,10)
    page_number = request.GET.get("page")
    page_obj = results.get_page(page_number)
    # print("bfgg",users.values())
    # return HttpResponse("hola")
    return render(request,'users/index.html',locals())

@login_required(login_url='/mngr/')
def adminLogout(request):
    logout(request)
    return redirect('adm_login')