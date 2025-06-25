from django.urls import path, include
from . import views
from .import forms
from .views import (
    ProductList, ProductCreate, ProductUpdate,  delete_image, delete_variant, Listado_Sup, exportar_excel
)



urlpatterns = [
    #path('', views.home, name="home"), 
    #path('form/', views.form, name='formulario'),
    #path('edit_form/<int:pk>', views.edit_form, name='edit_form'),
    path('', views.ProductList, name='list_products'),
    path('listados/', views.Listado_Sup, name='list_sup'),
    path('create/', ProductCreate.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdate.as_view(), name='update_product'),
    #path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('delete-variant/<int:pk>/', delete_variant, name='delete_variant'),
    path('search/', views.Busquedas, name='buscar'),
    path('exportar/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
]



