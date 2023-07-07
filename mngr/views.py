from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product,Sale
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .forms import ProductForm,StockUpdate,SaleUpdate
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
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

@login_required(login_url='/mngr/')
def profile(request):
    context = {}
    if request.user:
        profile = User.objects.get(pk = request.user.id)
        for key,value in profile.__dict__.items():
            print(f"{key} : {value}")
        context = {
            'profile' : profile
        }
        return render(request,'users/profile.html',context)
    else:
        return redirect('adm_login')
    
@login_required(login_url='/mngr/')
def editProduct(request,product_id):
    product = Product.objects.get(pk = product_id)
    
    if request.method =='POST':
        editForm = ProductForm(request.POST,instance = product)
        name = request.POST.get('name')
        
        check = Product.objects.filter(name = name).exclude(pk = product_id).first()
        
        if check is not None:
            # print(123)
            messages.warning(request,"This name is used already")
            return redirect('edit_product',product_id)
        else:
            # print(12345)
            if editForm.is_valid():
                editForm.save()
                messages.success(request,"Your product updated successfully")
                return redirect('product_list')
    
    form = ProductForm(instance = product)
    
    context = {
        'form' : form
    }
    
    return render(request,'products/edit.html',context)

@login_required(login_url='/mngr/')
def changePassword(request):
    
    if request.method =="POST":
        pswdForm = PasswordChangeForm(request.user,request.POST)
        
        if pswdForm.is_valid():
            pswdForm.save()
            messages.success(request,"Your password updated successfully")  # superadmin - cafeksa@123
            return redirect('adm_profile')
        else:
            # for field in pswdForm:
            #     for error in field.errors:
            #         print(error)
            messages.warning(request,"Something went wrong. Your password was not changed")
            return redirect('change_password')
    
    form = PasswordChangeForm(user = request.user)
    
    context = {
        'form' : form
    }
    # for key,value in form.__dict__.items():
    #     print(f"{key} = {value}")
    return render(request,'users/password_change.html',context)

@login_required(login_url='/mngr/')
def todaysOrder(request):
    if request.method =='POST':
        selling_date = request.POST.get('sell_date')
        productList = request.POST.getlist('product')
        sellCountList = request.POST.getlist('sell_count')
        productSaleCount =zip(request.POST.getlist('product'),request.POST.getlist('sell_count'))
        for product,sell_count in productSaleCount:
            
            checkProductStock = Product.objects.filter(id = product,stock__gte = sell_count).first()
            if checkProductStock is not None:
                # print("fff",checkProductStock._meta.get_fields())
                data_dict = {'product':product,'sell_count':sell_count,'sell_date':selling_date}
                form = SaleUpdate(data_dict)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.created_by = request.user
                    f.save()
                    
                    updProduct = checkProductStock.stock - int(sell_count)
                    checkProductStock.stock = updProduct
                    checkProductStock.save()
            
        
        sell_date = request.POST.get('sell_date')
        date = datetime.strptime(sell_date,'%Y-%m-%d') #convert string date to datetime object
        formattedDate = date.strftime("%B %d, %Y")
        
        messages.success(request,"Your sales report of "+formattedDate+" updated")
        return redirect('all_orders')
                
    todaySale = SaleUpdate()
    
    context = {
        'todaySale' : todaySale
    }
    # return HttpResponse('todays order')
    return render(request,'sales/today_sale.html',context)

@login_required(login_url='/stockUpdate/')
def stockUpdate(request,product_id):
    
    if request.method =='POST':
        product = Product.objects.get(pk = product_id)
        # print("product",product)
        form = StockUpdate(request.POST,instance=product)
        # print("form",form)
        if form.is_valid():
            form.save()
            messages.success(request,"Stock updated successfully")
            return redirect('product_list')
        
    stockForm = StockUpdate(initial={
        'name' : Product.objects.filter(id = product_id).first(),
        'stock' : Product.objects.filter(id = product_id).values_list('stock',flat=True).first()
    })
    # k =Product.objects.filter(id = product_id).values_list('stock',flat=True).first()
    # print("nnnnn",k)
    
    context ={
        'stockForm': stockForm
    }
    return render(request,'products/stock.html',context)

@login_required(login_url='/mngr/')
@csrf_exempt
def stockCount(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        stockCount = Product.objects.filter(id = product).values_list('stock',flat=True).first()
        return JsonResponse({
            'productStock':stockCount
        })

@login_required(login_url='/mngr/')
def allOrders(request):
    allOrders = Sale.objects.order_by('sell_date').all()
    grandTotal = allOrders.aggregate(total_sell_count = Sum('sell_count'))
    # print("grand",grandTotal['total_sell_count'])
    results = Paginator(allOrders,10)
    page_number = request.GET.get('page')
    page_obj = results.get_page(page_number)
    context = {
        'page_obj':page_obj,
        'grand_total':grandTotal['total_sell_count']
    }
    return render(request,'sales/all_orders.html',context)