from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(Departamento)
admin.site.register(Cliente)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Linea)
admin.site.register(Medida)
admin.site.register(Bodega)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'udm', 'costo_cif', 'factor', 'precio')
    list_filter = ('categoria', 'linea')
    search_fields = ('codigo', 'descripcion', 'categoria__nombre')
    fields = (('codigo', 'descripcion', 'tipo'), ('marca', 'categoria', 'linea'),
                ('udm', 'presentacion', 'uso'), ('costo_fob', 'costo_cif', 'factor', 'precio'),
                ('clasificacion', 'imagen'), ('aplica_impuesto', 'compra_local'))
    readonly_fields = ('codigo', 'precio', 'costo_fob', 'costo_cif', 'factor')
admin.site.register(Producto, ProductoAdmin)

class TcAdmin(ImportExportModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('fecha', 'oficial', 'venta', 'compra')
admin.site.register(TC, TcAdmin)

class DetalleFactura(admin.TabularInline):
    model = DetalleFactura
    extra = 0
    fields = ('producto', 'descripcion', 'cantidad', 'precio', 'costo', 'bodega', 'iva', 'descuento')

class FacturaAdmin(admin.ModelAdmin):
    inlines = [DetalleFactura]
admin.site.register(Factura, FacturaAdmin)
