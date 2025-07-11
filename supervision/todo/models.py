from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from django.contrib.auth.forms import UserCreationForm


# Create your models here.

class Relevamiento(models.Model):
    nombre = models.CharField(max_length=50)
    #imagen = models.ImageField(null=True, blank=True, upload_to='images/', default='images/sin_Imagen.png')
    año = models.IntegerField(default=0)
    sup_fecha = models.DateField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.nombre

class Product(models.Model):
    
    sup_fecha = models.DateField(blank=True, null=True, auto_now_add=True)
    relevamiento = models.ForeignKey(Relevamiento, on_delete=models.CASCADE,null=True, related_name='productos')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total_personas = models.IntegerField(default=0)
    encuestador = models.CharField(max_length=50,default='')
    ficha_numero = models.CharField(max_length=50,default='')
    contadas = models.IntegerField(default=0)
    obs = models.TextField(max_length=255,default='')

    provincia = models.BooleanField()
    partido = models.BooleanField()
    municipio = models.BooleanField()
    localidad = models.BooleanField()
    barrio = models.BooleanField()
    fraccion = models.BooleanField()
    radio = models.BooleanField()
    area = models.BooleanField()
    paraje = models.BooleanField()
    comunidad = models.BooleanField()
    calle_tipo = models.BooleanField()
    calle = models.BooleanField()
    altura = models.BooleanField()
    piso = models.BooleanField()
    departamento = models.BooleanField()
    torre_pasillo_escalera = models.BooleanField()
    entre_calle = models.BooleanField()
    y_calle = models.BooleanField()
    cp = models.BooleanField()
    manzana = models.BooleanField()
    telefono = models.BooleanField()
    vivienda_ubicada = models.BooleanField()
    vivienda_tipo = models.BooleanField()

    omision_miembros = models.BooleanField()
    inclusion_miembros = models.BooleanField()
    respondente_valido = models.BooleanField()

    asistio1 = models.BooleanField()
    asisttio2 = models.BooleanField()
    nivel_cursa1 = models.BooleanField()
    nivel_cursa2 = models.BooleanField()

    semana_anterior1 = models.BooleanField()
    semana_anterior2 = models.BooleanField()
    busco_trabajo1 = models.BooleanField()
    busco_trabajo2 = models.BooleanField()
    descuentan_o_aporta1 = models.BooleanField()
    descuentan_o_aporta2 = models.BooleanField()

    ingresos_laborales1 = models.BooleanField()
    ingresos_laborales2 = models.BooleanField()

    recibe_auh1 = models.BooleanField()
    recibe_auh2 = models.BooleanField()
    quienes1 = models.BooleanField()
    quienes2 = models.BooleanField()
    programa_social1 = models.BooleanField()
    programa_social2 =  models.BooleanField()

    cobertura1 = models.BooleanField()
    cobertura2 = models.BooleanField()
    cronica1 =  models.BooleanField()
    cronica2 = models.BooleanField()

    embarazada1 = models.BooleanField()
    embarazada2 = models.BooleanField()

    dificultad_permanente1 = models.BooleanField()
    dificultad_permanente2 = models.BooleanField()

    material_pisos = models.BooleanField()
    agua_proviene = models.BooleanField()
    tiene_baño = models.BooleanField()
    desague = models.BooleanField() 
    

    def __str__(self):
        return self.ficha_numero


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True
        )
    image = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.product.title


class Variant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
        )
    
        
    nro_persona = models.IntegerField(default=0)
    nombre = models.CharField(max_length=50,default='')
    fecha_nacimiento = models.BooleanField()
    años = models.BooleanField()
    meses = models.BooleanField()
    sexo = models.BooleanField()
    genero = models.BooleanField()
    apellido = models.BooleanField()
    parentesco_jefe = models.BooleanField()
    situacion_conyugal = models.BooleanField()
    pareja_de = models.BooleanField()
    madre_padre1 = models.BooleanField()
    madre_padre2 = models.BooleanField()
    documento_tipo = models.BooleanField()
    documento = models.BooleanField()
    pais = models.BooleanField()
    indigena = models.BooleanField()
    
    def __str__(self):
        return self.product.ficha_numero


class Fichas_Estado(models.Model):
    
    id = models.IntegerField(primary_key=True)
    ficha_numero = models.CharField(max_length=100)
    encuestador = models.CharField(max_length=100)
    sup_fecha = models.CharField(max_length=100)
    contadas = models.IntegerField(default=0)
    relevamiento = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)    
    identificacion_grave = models.IntegerField(default=0)
    identificacion_leve = models.IntegerField(default=0)
    respondente_educacion = models.IntegerField(default=0)
    respondente_discapacidad = models.IntegerField(default=0)
    respondente_embarazo = models.IntegerField(default=0)
    respondente_ingresos = models.IntegerField(default=0)
    respondente_psociales = models.IntegerField(default=0)
    respondente_salud = models.IntegerField(default=0)
    respondente_trabajo = models.IntegerField(default=0)
    menor_educacion = models.IntegerField(default=0)
    menor_discapacidad = models.IntegerField(default=0)
    menor_embarazo = models.IntegerField(default=0)
    menor_ingresos = models.IntegerField(default=0)
    menor_psociales = models.IntegerField(default=0)
    menor_salud = models.IntegerField(default=0)
    menor_trabajo = models.IntegerField(default=0)
    domicilio = models.IntegerField(default=0)
    vivienda = models.IntegerField(default=0)
    conf_hogar = models.IntegerField(default=0)
    
    class Meta:
        managed = False  # Django no intentará crear ni borrar esta tabla
        db_table = 'vista_estado_fichas'  # Debe coincidir con el nombre de la vista




