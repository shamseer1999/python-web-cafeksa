from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.adminLogin,name='adm_login'),
    path('dashboard/',views.index,name='dashboard'),
    path('products/',views.productsList,name='product_list'),
    path('users/',views.usersList,name='user_list'),
    path('product/add-product',views.addProduct,name='add_product'),
    path('logout/',views.adminLogout,name='adm_logout'),
    path('profile/',views.profile,name='adm_profile'),
    path('product/edit-product/<int:product_id>',views.editProduct,name='edit_product')
]
