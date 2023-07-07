import django_filters
from .models import *
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model() 

class DateInput(forms.DateInput):
    input_type='date'

class SaleFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=forms.Select(
            attrs={'class':'form-control form-control-sm'}
            )
        )
    sell_date = django_filters.DateFilter(
        widget = DateInput(attrs={'class':'form-control form-control-sm'})
    ) 
    class Meta:
        model = Sale
        fields = ['sell_date','product']
        
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        widget = forms.TextInput(attrs={'class':'form-control'}),lookup_expr='icontains'
    )
    class Meta:
        model = Product
        fields = ['name']
        
class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        widget = forms.TextInput(attrs={'class':'form-control form-control-sm'})
        )
    is_staff = django_filters.BooleanFilter(
        widget = forms.Select(choices=[('','-----'),(True,'Yes'),(False,'No')], attrs={'class':'form-control form-control-sm'})
    )
    class Meta:
        model = User
        fields = ['username','is_staff']
        
