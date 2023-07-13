from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'marca', 'stock', 'precio', 'categoria', 'imagen']
        labels = {
            'codigo': 'Codigo',
            'nombre': 'Nombre',
            'marca': 'Marca',
            'stock': 'Stock',
            'precio': 'Precio',
            'categoria': 'Categoria',
            'imagen': 'Imagen'
        }
        widgets = {
            'codigo': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese codigo..',
                    'id': 'codigo',
                    'class': 'form-control',
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre..',
                    'id': 'nombre',
                    'class': 'form-control',
                }
            ),
            'marca': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese marca..',
                    'id': 'marca',
                    'class': 'form-control',
                }
            ),
            'stock': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese stock..',
                    'id': 'stock',
                    'class': 'form-control',
                }
            ),
            'precio': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese precio..',
                    'id': 'precio',
                    'class': 'form-control',
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'id': 'categoria',
                    'class': 'form-control',
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'imagen',
                }
            )
        }

