from django.contrib import admin
from .models import Product,Sale
# Register your models here.

# admin.site.register(Product)
# class ReadonlyAdminMixin:
#     #override permission
#     def has_add_permission(self,request):
#         return False
#     def has_change_permission(self,request,obj=None):
#         if request.user.has_perm('mngr.delete_product'):
#             return True
#         else:
#             return False
#     def has_delete_permission(self,request,obj=None):
#         return False
#     def has_view_permission(self,request,obj=None):
#         is_superuser = request.user.is_superuser
#         return True
#         # if is_superuser:
#         #     return True
#         # else:
#         #     return False
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","description","stock","created_by","created_at")
    
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("sell_date","product","sell_count","created_by","created_at")
    
    
