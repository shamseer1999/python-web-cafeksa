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
        if Product.objects.filter(name = data).exists():
            raise ValidationError('This name is used already')
        else:
            return data