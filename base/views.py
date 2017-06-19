from django.shortcuts import render
from .models import *
from django.shortcuts import HttpResponse

def obtener_producto(request):
    codigo = request.POST.get('codigo', None)
    return HttpResponse('aplication/json', Producto.objects.get(codigo=codigo).to_json())


def imprimir_factura(request):
    factura = Factura.objects.get(id=int(request.GET.get('id')))
    return render(request, "print/factura.html", {'factura': factura})
