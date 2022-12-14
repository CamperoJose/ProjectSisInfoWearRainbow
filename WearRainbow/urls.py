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
from django.conf.urls import handler404

from . import views

# add a flag for
# handling the 404 error
'''
handler404 = 'pages.views.Error404View'
handler500 = 'pages.views.Error404View'
'''

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.paginaIndex, name="paginaIndex"),
    path('registrarpersona', views.registroPersona, name="registrarPersona"),
    path('registroPedido/', views.registroPedido, name="registroPedido"),
    path('SignInAsClient/', views.SignInAsClient, name="SignInAsClient"),
    path('OrderForm/', views.OrderForm, name="OrderForm"),
    path('SignInAsAdministrator/', views.SignInAsAdministrator, name="SignInAsAdministrator"),
    path('ClientPanel/', views.ClientPanel, name="ClientPanel"),
    path('OrdersAdministrator/', views.OrdersAdministrator, name="OrdersAdministrator"),
    path('Carrito/', views.Carrito, name="Carrito"),
    path('DepartamentsAdministrator/', views.DepartamentsAdministrator, name="DepartamentsAdministrator"),
    path('CategoriesAdministrator/', views.CategoriesAdministrator, name="CategoriesAdministrator"),
    path('SizesAdministrator/', views.SizesAdministrator, name="SizesAdministrator"),
    path('ProductsAdministrator/', views.ProductsAdministrator, name="ProductsAdministrator"),
    path('productsAsClient/', views.productsAsClient, name="productsAsClient"),
    path('AddNewProduct/', views.AddNewProduct, name="AddNewProduct"),
    path('registroProducto/', views.registroProducto, name="registroProducto"),
    path('contacts/', views.contacts, name="contacts"),
    path('registroTalla/', views.registroTalla, name="registroTalla"),
    path('modificarTalla/<id>', views.modificarTalla, name="modificarTalla"),
    path('ModifyProduct/<id>', views.ModifyProduct, name="ModifyProduct"),
    path('DetallePedidio/<id>', views.DetallePedidio, name="DetallePedidio"),
    path('DetallePedidoCliente/<id>', views.DetallePedidoCliente, name="DetallePedidoCliente"),
    path('ViewProduct/<id>', views.ViewProduct, name="ViewProduct"),
    path('ViewProductClient/<id>', views.ViewProductClient, name="ViewProductClient"),
    path('OrdersAsClient/', views.OrdersAsClient, name="OrdersAsClient"),
    path('modificarProducto/', views.modificarProducto, name="modificarProducto"),
    path('addCart/<id>', views.addCart, name="addCart"),
    path('deleteItem/<id>', views.deleteItem, name="deleteItem"),
    path('registroCategoria/', views.registroCategoria, name="registroCategoria"),
    path('modificarCategoria/<id>', views.modificarCategoria, name="modificarCategoria"),
    path('registroDepartamentos/', views.registroDepartamentos, name="registroDepartamentos"),
    path('modificarDepartamento/<id>', views.modificarDepartamento, name="modificarDepartamento"),
    path('registrarCliente/', views.registroCliente, name="registrarCliente"),
    path('inicioSesionCliente/', views.inicioSesionCliente, name="inicioSesionCliente"),
    path('inicioSesionAdministrador/', views.inicioSesionAdministrador, name="inicioSesionAdministrador"),
    path('PedidosSeleccionados/', views.PedidosSeleccionados, name="PedidosSeleccionados"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('administratorManager/', views.administratorManager, name="administratorManager"),
    path('PaymentDetails01/<id>', views.PaymentDetails01, name="PaymentDetails01"),
    path('PaymentDetails02/<id>', views.PaymentDetails02, name="PaymentDetails02"),
    path('PaymentDetails03/<id>', views.PaymentDetails03, name="PaymentDetails03"),
    path('registroPago/<id>', views.registroPago, name="registroPago"),
    path('registroPedidoAceptado/<id>', views.registroPedidoAceptado, name="registroPedidoAceptado"),
    path('registroPedidoRechazado/<id>', views.registroPedidoRechazado, name="registroPedidoRechazado"),
    path('registroPedidoEnviado/<id>', views.registroPedidoEnviado, name="registroPedidoEnviado"),
    path('modificarAcceso/<id>', views.modificarAcceso, name="modificarAcceso"),
    path('addAdministrador/', views.addAdministrador, name="addAdministrador"),
    path('Logout/', views.Logout, name="Logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

