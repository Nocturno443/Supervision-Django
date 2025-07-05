from django.shortcuts import get_object_or_404,render,redirect
from django.contrib import messages
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from .forms import (
    ProductForm, VariantFormSet, ImageFormSet
)
from .models import (
    Image,
    Product,
    Variant,
    Relevamiento
)
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa #sirve para transformar en pdf
from io import BytesIO
from openpyxl import Workbook #sirve para exportar a Exell
from django.utils.text import slugify
import datetime


# Create your views here.

class ProductInline():
    form_class = ProductForm
    model = Product
    template_name = "product_create_or_update.html"
    
    def __init__(self):
        self.contestados1 = 0
        self.contestados2 = 0

    def incrementar_contador(self):
        self.contestados1 += 1
        
        return self.contestados1

    #def incrementar_contador2(self):
    #    self.contestados2 += 1

    #def sumar_valores(self):
    #    total = self.contestados1 + self.contestados2
    #    return total
    

    def form_valid(self, form):
       
        campos_contestados = form.clean()
        
        #contestados=0
         

        for campo in campos_contestados:
            if campos_contestados[campo] is True:
                self.contestados1 +=1
                #self.incrementar_contador()


        named_formsets = self.get_named_formsets()
        
        #num_contestados = form.cleaned_data['provincia']
        
        print(f"Número de campos contestados: {self.contestados1}", flush=True)
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        #self.object.contadas=self.contestados1
        #self.object.user=User.objects.get(user=request.user)
        #self.object.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
                     

            if formset_save_func is not None:

                for form in formset:
            
                    if form.cleaned_data:
                        #contestados2=form.cleaned_data['sexo']
                        for campo in form.cleaned_data:
                            if form.cleaned_data[campo] is True:
                                self.contestados1 +=1
                                self.object.contadas=self.contestados1

                print(f"Número de campos contestados personas: {self.contestados1}", flush=True)

                self.object.save()
                formset_save_func(formset)
            else:
                self.object.save()
                formset.save()
                
        return redirect('list_products')

    def formset_variants_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
         

        #for form in formset:
            
            #if form.cleaned_data:
                #contestados2=form.cleaned_data['sexo']
             #   for campo in form.cleaned_data:
                    #if form.cleaned_data[campo] is True:
                    #    self.contestados1 +=1
                    #    form.instance.contadas2 = self.contestados1
        
        #print(f"Número de campos contestados personas: {self.contestados1}", flush=True)
        
        variants = formset.save(commit=False)  # self.save_formset(formset, contact)
        
              

        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:

            
            variant.product = self.object
            
            
            
            variant.save()

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.product = self.object
            image.save()

            
class ProductCreate(ProductInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': VariantFormSet(prefix='variants'),
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }


class ProductUpdate(ProductInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }
    
    def __init__(self):
        self.contestados1 = 0
        self.contestados2 = 0


    
class ProductList_old(ListView):
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        if self.request.user.is_authenticated:
                return Product.objects.filter(user=self.request.user).order_by('-sup_fecha')    

        else:
         messages.success(self.request,("Tenes que estar logueado"))
         return render(self.request, 'login.html', {})
        

def ProductList(request):
    if request.user.is_authenticated:
        productos_filtrados = Product.objects.select_related('relevamiento').filter(user=request.user).order_by('-sup_fecha')
        
        # Agrupamos los productos por relevamiento
        relevamientos_con_productos = {}
        for producto in productos_filtrados:
            r = producto.relevamiento
            relevamientos_con_productos.setdefault(r, []).append(producto)

        return render(request, 'product_list.html', {
            'resultados': relevamientos_con_productos,
            
        })
    else:
         messages.success(request,("Tenes que estar logueado"))
         return render(request, 'login.html', {})



'''This 2 functions are for custom added delete button functionality. If you don't want to use custom delete buttons than don't add this'''

def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('update_product', pk=image.product.id)

    image.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('update_product', pk=image.product.id)


def delete_variant(request, pk):
    try:
        variant = Variant.objects.get(id=pk)
    except Variant.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('update_product', pk=variant.product.id)

    variant.delete()
    messages.success(
            request, 'Variant deleted successfully'
            )
    return redirect('update_product', pk=variant.product.id)
   

def Listado_Sup(request):
     if request.user.is_authenticated:
        relevamientos = Relevamiento.objects.prefetch_related('productos')
        print("relevamientos:", relevamientos)
        # return render(request, 'listados.html', {'relevamientos': relevamientos})
       
  
        return render(request, 'listados.html', {'relevamientos': relevamientos})
     
     else:
         messages.success(request,("Tenes que estar logueado"))
         return render(request, 'login.html', {})

   

def Busquedas(request):
    searched = request.POST.get('searched', '')
    productos_filtrados = Product.objects.select_related('relevamiento').filter(
        Q(encuestador__icontains=searched) |
        Q(ficha_numero__icontains=searched) |
        Q(relevamiento__nombre__icontains=searched)

    )

    # Agrupamos los productos por relevamiento
    relevamientos_con_productos = {}
    for producto in productos_filtrados:
        r = producto.relevamiento
        relevamientos_con_productos.setdefault(r, []).append(producto)

    return render(request, 'search_sup.html', {
        'resultados': relevamientos_con_productos,
        'searched': searched
    })


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def exportar_pdf(request):
    searched = request.GET.get('q', '')
    productos_filtrados = Product.objects.select_related('relevamiento').filter(
        Q(encuestador__icontains=searched) |
        Q(ficha_numero__icontains=searched) |
        Q(relevamiento__nombre__icontains=searched)

    )

    # Agrupamos los productos por relevamiento
    relevamientos_con_productos = {}
    for producto in productos_filtrados:
        r = producto.relevamiento
        relevamientos_con_productos.setdefault(r, []).append(producto)

    context = {
        'resultados': relevamientos_con_productos,
        'searched': searched,
        'request': request  # necesario para rutas absolutas
    }

    return render_to_pdf('exportar_pdf.html', context)

    
def exportar_excel(request):
    searched = request.GET.get('q', '')
    print("Buscando:", searched)
    productos_filtrados = Product.objects.select_related('relevamiento').filter(
        Q(encuestador__icontains=searched) |
        Q(ficha_numero__icontains=searched) |
        Q(relevamiento__nombre__icontains=searched)

    )

    # Agrupamos los productos por relevamiento
    relevamientos_con_productos = {}
    for producto in productos_filtrados:
        r = producto.relevamiento
        relevamientos_con_productos.setdefault(r, []).append(producto)


    wb = Workbook()
    ws = wb.active
    ws.title = "Productos"

    # Encabezados
    columnas = ["Ficha", "Encuestador", "Supervisor", "Relevamiento", "Cant.Pers.", "Errores", "Estado","Fecha"]
    ws.append(columnas)

    # Datos
    for p in productos_filtrados:
        ws.append([
            p.ficha_numero,
            p.encuestador,
            str(p.user), 
            str(p.relevamiento),
            p.total_personas,
            p.contadas,
            'APROBADA' if p.contadas < 7 else 'RECHAZADA',
            p.sup_fecha.strftime('%Y-%m-%d') if p.sup_fecha else ''
        ])
    
    hoy = datetime.datetime.now().strftime('%Y-%m-%d')
    informe = 'Supervision'
    filename = f"Listado_{slugify(informe)}_{hoy}.xlsx"
    
    # Respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response




















    

