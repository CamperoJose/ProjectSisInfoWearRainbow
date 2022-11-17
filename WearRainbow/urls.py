"""WearRainbow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.paginaIndex, name="paginaIndex"),
    path('registrarpersona', views.registroPersona, name="registrarPersona"),
    path('SignInAsClient/', views.SignInAsClient, name="SignInAsClient"),
    path('SignInAsAdministrator/', views.SignInAsAdministrator, name="SignInAsAdministrator"),
    path('ClientPanel/', views.ClientPanel, name="ClientPanel"),
    path('OrdersAdministrator/', views.OrdersAdministrator, name="OrdersAdministrator"),
    path('Carrito/', views.Carrito, name="Carrito"),
    path('CategoriesAdministrator/', views.CategoriesAdministrator, name="CategoriesAdministrator"),
    path('SizesAdministrator/', views.SizesAdministrator, name="SizesAdministrator"),
    path('ProductsAdministrator/', views.ProductsAdministrator, name="ProductsAdministrator"),
    path('productsAsClient/', views.productsAsClient, name="productsAsClient"),
    path('AddNewProduct/', views.AddNewProduct, name="AddNewProduct"),
    path('registroProducto/', views.registroProducto, name="registroProducto"),
    path('contacts/', views.contacts, name="contacts"),
    path('registroTalla/', views.registroTalla, name="registroTalla"),
    path('ModifyProduct/<id>', views.ModifyProduct, name="ModifyProduct"),
    path('ViewProduct/<id>', views.ViewProduct, name="ViewProduct"),
    path('ViewProductClient/<id>', views.ViewProductClient, name="ViewProductClient"),
    path('modificarProducto/', views.modificarProducto, name="modificarProducto"),
    path('addCart/<id>', views.addCart, name="addCart"),
    path('registroCategoria/', views.registroCategoria, name="registroCategoria"),
    path('registrarCliente/', views.registroCliente, name="registrarCliente"),
    path('inicioSesionCliente/', views.inicioSesionCliente, name="inicioSesionCliente"),
    path('inicioSesionAdministrador/', views.inicioSesionAdministrador, name="inicioSesionAdministrador"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

