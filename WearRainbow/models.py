from django.db import models
from django.db.models import Avg, Count, Min, Sum


class persona(models.Model):
    id_persona = models.AutoField(primary_key=True, null=False, unique=True)
    nombre = models.CharField(max_length=30, null=False)
    apellidoPaterno = models.CharField(max_length=30, null=False)
    apellidoMaterno = models.CharField(max_length=30, null=False)
    ciNumero = models.CharField(max_length=30, null=False, unique=True)
    ciExtension = models.CharField(max_length=30, null=False)
    ciComplemento = models.CharField(max_length=30, null=False)
    celular = models.CharField(max_length=30, null=False)
    correo = models.CharField(max_length=30, null=False)

    def get_nombre(self):
        return self.nombre

    def get_id_persona(self):
        return self.id_persona


class administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True, null=False, unique=True)
    id_persona = models.ForeignKey(persona, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=30, null=False)
    contraseña = models.CharField(max_length=30, null=False)

    def get_id_administrador(self):
        return self.id_administrador

    def get_id_persona(self):
        return self.id_persona

    def get_usuario(self):
        return self.usuario

    def get_contraseña(self):
        return self.contraseña


class cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, null=False, unique=True)
    id_persona = models.ForeignKey(persona, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=30, null=False)
    contraseña = models.CharField(max_length=30, null=False)

    def get_id_cliente(self):
        return self.id_cliente

    def get_id_persona(self):
        return self.id_persona

    def get_usuario(self):
        return self.usuario

    def get_contraseña(self):
        return self.contraseña


class Talla(models.Model):
    id_talla = models.AutoField(primary_key=True, null=False, unique=True)
    talla = models.CharField(max_length=30, null=False)
    largoEspalda = models.IntegerField(null=False)
    contornoPecho = models.IntegerField(null=False)
    contornoCuello = models.IntegerField(null=False)

    def get_id_talla(self):
        return self.id_talla

    def get_talla(self):
        return self.talla

    def get_catidadTallas(self):
        return Talla.objects.count()

    def get_id_largoEspalda(self):
        return self.largoEspalda

    def get_id_contornoPecho(self):
        return self.contornoPecho

    def get_id_contornoCuello(self):
        return self.contornoCuello

    def __str__(self):
        return self.talla


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, null=False, unique=True)
    categoria = models.CharField(max_length=30, null=False)

    def get_id_categoria(self):
        return self.id_categoria

    def get_categoria(self):
        return self.categoria

    def __str__(self):
        return self.categoria


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, null=False, unique=True)
    nombre = models.CharField(max_length=30, null=False)
    descripcion = models.CharField(max_length=300, null=False)
    color = models.CharField(max_length=30, null=False)
    precio = models.FloatField(null=False)
    material = models.CharField(max_length=30, null=False)
    img = models.ImageField(upload_to="images/", null=False)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def get_id_producto(self):
        return self.id_producto

    def get_price(self):
        return round(self.precio, 1)

    def get_id_cat(self):
        return self.id_categoria

    def get_cant_talla(self):
        obj = TallaDisponible.objects.get(id_producto=self.id_producto)
        print(obj)
        return obj


    def get_total_stock(self):
        obj = TallaDisponible.objects.filter(id_producto=self.id_producto).aggregate(Sum('stock'))
        if obj['stock__sum'] == None:
            return 0
        return obj['stock__sum']


class TallaDisponible(models.Model):
    id_tallaDisponible = models.AutoField(primary_key=True, null=False, unique=True)
    stock = models.IntegerField(null=False)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_talla = models.ForeignKey(Talla, on_delete=models.CASCADE)

    def get_stock(self):
        return self.stock

    def get_id_talla(self):
        return str(self.id_talla)

    def __str__(self):
        return self.id_talla






class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True, null=False, unique=True)
    Departamento = models.CharField(max_length=30, null=False)
