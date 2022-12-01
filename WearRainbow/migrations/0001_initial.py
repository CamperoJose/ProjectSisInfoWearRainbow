# Generated by Django 2.1.15 on 2022-12-01 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='administrador',
            fields=[
                ('id_administrador', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('usuario', models.CharField(max_length=30)),
                ('contraseña', models.CharField(max_length=500)),
                ('rol', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('categoria', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('usuario', models.CharField(max_length=30)),
                ('contraseña', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id_departamento', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Departamento', models.CharField(max_length=30)),
                ('precio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Comprobante', models.ImageField(upload_to='comprobantesPago/')),
                ('BancoProveniente', models.CharField(max_length=150)),
                ('MetodoPago', models.CharField(max_length=150)),
                ('FechaPago', models.DateTimeField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('TotalPagar', models.FloatField()),
                ('Direccion', models.CharField(max_length=150)),
                ('Zona', models.CharField(max_length=50)),
                ('Apartamento', models.CharField(max_length=50)),
                ('EstadoPedido', models.CharField(max_length=50)),
                ('FechaPedido', models.DateTimeField(max_length=50)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.cliente')),
                ('id_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoAceptado',
            fields=[
                ('id_pedidoAceptado', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('FechaAceptacion', models.DateTimeField()),
                ('FechaEnvio', models.DateTimeField(null=True)),
                ('id_administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.administrador')),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoRechazado',
            fields=[
                ('id_pedidoAceptado', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('FechaRechazo', models.DateTimeField()),
                ('RazonRechazo', models.CharField(max_length=150)),
                ('id_administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.administrador')),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='persona',
            fields=[
                ('id_persona', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=30)),
                ('apellidoPaterno', models.CharField(max_length=30)),
                ('apellidoMaterno', models.CharField(max_length=30)),
                ('ciNumero', models.CharField(max_length=30, unique=True)),
                ('ciExtension', models.CharField(max_length=30)),
                ('ciComplemento', models.CharField(max_length=30)),
                ('celular', models.CharField(max_length=30)),
                ('correo', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=300)),
                ('color', models.CharField(max_length=30)),
                ('precio', models.FloatField()),
                ('material', models.CharField(max_length=30)),
                ('img', models.ImageField(upload_to='images/')),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='ProductosPedido',
            fields=[
                ('id_productoPedido', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cantidad', models.IntegerField()),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Talla',
            fields=[
                ('id_talla', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('talla', models.CharField(max_length=30)),
                ('largoEspalda', models.IntegerField()),
                ('contornoPecho', models.IntegerField()),
                ('contornoCuello', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TallaDisponible',
            fields=[
                ('id_tallaDisponible', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('stock', models.IntegerField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Producto')),
                ('id_talla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Talla')),
            ],
        ),
        migrations.AddField(
            model_name='productospedido',
            name='id_tallaDisponible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.TallaDisponible'),
        ),
        migrations.AddField(
            model_name='pago',
            name='id_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.Pedido'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='id_persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.persona'),
        ),
        migrations.AddField(
            model_name='administrador',
            name='id_persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WearRainbow.persona'),
        ),
    ]