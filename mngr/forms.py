from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','description','created_by')
        
    def __init__(self,*args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm','required':'required'})
              
            
    def clean_name(self):
        data = self.cleaned_data['name']
        if self.instance.pk is None:   #check it is a new object
            if Product.objects.filter(name = data).exists():
                raise ValidationError('This name is used already')
        else:
            return data
        
class StockUpdate(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'stock')
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control form-control-sm','readonly':True}),
            'stock' : forms.NumberInput(attrs={'class':'form-control form-control-sm'})
        }