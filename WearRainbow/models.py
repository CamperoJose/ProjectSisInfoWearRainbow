from django.db import models


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

    def get_id_talla(self):
        return self.talla

    def get_id_largoEspalda(self):
        return self.largoEspalda

    def get_id_contornoPecho(self):
        return self.contornoPecho

    def get_id_contornoCuello(self):
        return self.contornoCuello


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, null=False, unique=True)
    categoria = models.CharField(max_length=30, null=False)
    def get_id_categoria(self):
        return self.id_categoria
    def get_categoria(self):
        return self.categoria
