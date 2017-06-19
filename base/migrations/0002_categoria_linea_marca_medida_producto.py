# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-13 21:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Linea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8)),
                ('tipo', models.IntegerField(choices=[(1, 'Producto'), (2, 'Servicio')], default=1)),
                ('descripcion', models.CharField(max_length=100)),
                ('presentacion', models.CharField(max_length=10)),
                ('uso', models.IntegerField(choices=[(1, 'Industrial'), (2, 'Automotriz'), (3, 'Otros')], default=1)),
                ('clasificacion', models.CharField(blank=True, max_length=3, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='Imagenes')),
                ('costo_fob', models.PositiveIntegerField(default=0.0)),
                ('costo_cif', models.PositiveIntegerField(default=0.0)),
                ('factor', models.PositiveIntegerField(default=0.0)),
                ('precio', models.PositiveIntegerField(default=0.0)),
                ('aplica_impuesto', models.BooleanField(default=0.0)),
                ('compra_local', models.BooleanField(default=0.0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Categoria')),
                ('linea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Linea')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Marca')),
                ('udm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Medida')),
            ],
        ),
    ]
