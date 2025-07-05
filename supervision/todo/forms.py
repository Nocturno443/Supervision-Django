from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from .models import (
    Product, Image, Variant, Relevamiento
)


class ProductForm(forms.ModelForm):

   #contadas = forms.NumberInput()

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user']
                
        widgets = {
            
            'encuestador': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            
            'relevamiento': forms.Select(attrs={'class': 'form-control'}),


            'ficha_numero': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'total_personas': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ), 
            'contadas': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ), 
             'obs': forms.Textarea(
                attrs={
                    'class': 'form-control'
                    }
                ),         
        }

    def clean(self):
        super().clean()

        campos_contestados = 0

        for campo in self.cleaned_data:
            if self.cleaned_data[campo] is True:
                campos_contestados +=1

        self.num_campos_contestados = campos_contestados
        return self.cleaned_data
    
    
    def clean_ficha_numero(self):
        ficha = self.cleaned_data['ficha_numero']
        if Product.objects.filter(ficha_numero=ficha).exists():
            raise forms.ValidationError("Este número de ficha ya fue procesado.")
        return ficha

    

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'


class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'nro_persona': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            
        }

            

VariantFormSet = inlineformset_factory(
    Product, Variant, form=VariantForm,
    extra=1, can_delete=True, can_delete_extra=True
)

ImageFormSet = inlineformset_factory(
    Product, Image, form=ImageForm,
    extra=1, can_delete=True, can_delete_extra=True
)

