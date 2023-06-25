from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.adminLogin,name='adm_login'),
    path('dashboard/',views.index,name='dashboard'),
    path('logout/',views.adminLogout,name='adm_logout')
]
