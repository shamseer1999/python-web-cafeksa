from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.adminLogin,name='adm_login'),
    path('dashboard/',views.index,name='dashboard'),
    path('products/',views.productsList,name='product_list'),
    path('users/',views.usersList,name='user_list'),
    path('product/add-product',views.addProduct,name='add_product'),
    path('logout/',views.adminLogout,name='adm_logout')
]
