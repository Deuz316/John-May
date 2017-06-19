from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.forms.models import model_to_dict


class Base(models.Model):
    def to_json(self):
        return model_to_dic(self)

    class Meta:
        abstract = True


SECTORES = (
(1, 'AGROPECUARIO'),
(2, 'AGUA'),
(3, 'COMERCIO'),
(4, 'CONSTRUCCION'),
(5, 'DEFENSA'),
(6, 'ENERGIA'),
(7, 'GOBIERNO'),
(8, 'INDUSTRIA'),
(9, 'INGENIOS'),
(10, 'PESCA'),
(11, 'MINERIA'),
(12, 'TRANSPORTE'),
(13, 'OTROS'),
(14, 'ESTACIONES DE SERVICIO'),
)

TIPOS = ((1,'NATURAL'),(2,'JURIDICO'))

TIPO_PRODUCTO = ((1,'Producto'),(2,'Servicio'))

USO_PRODUCTO = ((1, 'Industrial'),(2, 'Automotriz'),(3, 'Otros'))

AFECTACIONES = ((1, 'POSITIVA'),(-1, 'NEGATIVA'),(0, 'SIN AFECTACION'))


MONEDAS = ((1, 'CORDOBAS'), (2, 'DOLARES'))


class TC(Base):
    fecha = models.DateField()
    oficial = models.FloatField()
    venta = models.FloatField(null=True, blank=True)
    compra = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return '{} {}'.format(self.fecha, self.oficial)

    def tc_venta(self):
        if self.venta:
            return self.venta
        else:
            return self.oficial

    def tc_compra(self):
        if self.compra:
            return self.compra
        else:
            return self.oficial

    class Meta:
        verbose_name = "tasa de cambio"
        verbose_name_plural = "tasas de cambio"

def dolarizar(monto=1, fecha=datetime.now()):
    return monto / TC.objects.get(fecha=fecha).tc_venta()

def cordobizar(monto=1, fecha=datetime.now()):
    return monto * TC.objects.get(fecha=fecha).tc_compra()

class Entidad(Base):
    codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre

    class Meta:
        abstract = True


class Departamento(Entidad):
    pass


class Marca(Entidad):
    pass


class Categoria(Entidad):
    pass


class Linea(Entidad):
    pass


class Medida(Entidad):
    pass


class Bodega(Entidad):
    pass


class Existencia(Base):
    producto = models.ForeignKey('Producto')
    bodega = models.ForeignKey(Bodega)
    existencia = models.FloatField(default=0.0)
    disponibilidad = models.FloatField(default=0.0)
    ubicacion = models.CharField(max_length=15, null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)


class BaseCliente(Base):
    nombre = models.CharField(max_length=255, verbose_name="razon social")
    identificacion = models.CharField(max_length=14, verbose_name="RUC/CEDULA")
    telefono = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)

    class Meta:
        abstract = True


class Cliente(BaseCliente):
    tipo = models.IntegerField(choices=TIPOS, default=1)
    departamento = models.ForeignKey(Departamento)
    sector = models.IntegerField(choices=SECTORES, default=1)
    clasificacion = models.CharField(max_length=3, null=True, blank=True)
    limite_credito = models.FloatField(default=0.0)
    limite_descuento = models.FloatField(default=0.0)
    plazo = models.PositiveIntegerField(default=0, help_text="plazo de credito en dias")
    saldo = models.FloatField(default=0.0)
    mora = models.FloatField(default=0.0, verbose_name="saldo en mora")

    def __unicode__(self):
        return '{} {}'.format(self.nombre, self.identificacion)

    def calcular_saldo(self):
        return 0.0

    def saldo_mora(self):
        return 0.0

    def clasificar(self):
        self.clasificacion = 'AAA'
        self.save()

class DatosCliente(BaseCliente):
    cliente = models.ForeignKey(Cliente, related_name="%(app_label)s_%(class)s_cliente")


class BaseProducto(Base):
    codigo = models.CharField(max_length=8, null=True)
    descripcion = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True


class Producto(BaseProducto):
    tipo = models.IntegerField(choices=TIPO_PRODUCTO, default=1)
    marca = models.ForeignKey(Marca)
    categoria = models.ForeignKey(Categoria)
    linea = models.ForeignKey(Linea)
    udm = models.ForeignKey(Medida)
    presentacion = models.CharField(max_length=10)
    uso = models.IntegerField(choices=USO_PRODUCTO, default=1)
    clasificacion = models.CharField(max_length=3, null=True, blank=True)
    imagen = models.ImageField(upload_to="Imagenes", null=True, blank=True)
    costo_fob = models.PositiveIntegerField(default=0.0)
    costo_cif = models.PositiveIntegerField(default=0.0)
    factor = models.PositiveIntegerField(default=0.0)
    precio = models.PositiveIntegerField(default=0.0)
    aplica_impuesto = models.BooleanField(default=0.0)
    compra_local = models.BooleanField(default=0.0)

    def calcular_costos(self):
        return 0.0

    def calcular_precio(self):
        return 0.0

    def clasificar(self):
        self.clasificacion = 'AAA'
        self.save()

    def __unicode__(self):
        return self.descripcion


class DatosProducto(BaseProducto):
    producto = models.ForeignKey(Producto, related_name="%(app_label)s_%(class)s_producto", null=True)

    class Meta:
        abstract = True


class Documento(Base):
    numero = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    afecta_costo = models.BooleanField(default=False)
    afecta_existencia = models.BooleanField(default=False)
    afectacion = models.IntegerField(choices=AFECTACIONES, default=0)

    class Meta:
        abstract = True


class Factura(Documento, DatosCliente):
    def detalle(self):
        return DetalleFactura.objects.filter(factura=self)


class DetalleFactura(DatosProducto):
    factura = models.ForeignKey(Factura)
    cantidad = models.FloatField(default=0.0)
    precio = models.FloatField(default=0.0)
    costo = models.FloatField(default=0.0)
    costo_promedio = models.FloatField(default=0.0)
    bodega = models.ForeignKey(Bodega)
    iva = models.PositiveIntegerField()
    descuento = models.PositiveIntegerField(default=0.0)
    existencia = models.FloatField(default=0.0)
    saldo = models.FloatField(default=0.0)

    def total(self):
        return self.precio * self.cantidad
