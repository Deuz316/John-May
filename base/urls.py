from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^imprimir_factura/', imprimir_factura, name="imprimir_factura"),
]
