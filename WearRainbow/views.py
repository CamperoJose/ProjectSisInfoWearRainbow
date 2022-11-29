import base64
from datetime import datetime, date
from idlelib import window

from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from WearRainbow import models
from WearRainbow.access import keyToken, keyBD
from WearRainbow.models import persona, administrador, Producto, Categoria, Talla, TallaDisponible, Departamento, \
    Pedido, ProductosPedido, Pago, PedidoAceptado, PedidoRechazado
from WearRainbow.models import cliente
from django.contrib import messages
from cryptography.fernet import Fernet

def sesiones(request):
    val=''
    if request.session.get('token_cliente'):
        val = 'Cliente'
    elif request.session.get('token_administrador'):
        val = 'Administrador'
    elif request.session.get('token_Superadministrador'):
        val = 'Superadministrador'
    return val


def paginaIndex(request):
    val = sesiones(request)
    return render(request, 'index.html', {'Sesion': val})

def PaymentDetails01(request, id):
    val = sesiones(request)
    pedido = Pedido.objects.get(id_pedido=id)
    return render(request, 'PaymentDetails01.html', {"pedido": pedido,'Sesion': val})


def PaymentDetails02(request, id):
    val = sesiones(request)
    pedido = Pedido.objects.get(id_pedido=id)
    return render(request, 'PaymentDetails02.html', {"pedido": pedido,'Sesion': val})


def PaymentDetails03(request, id):
    val = sesiones(request)
    pedido = Pedido.objects.get(id_pedido=id)
    return render(request, 'PaymentDetails03.html', {"pedido": pedido,'Sesion': val})


def OrdersAsClient(request):
    val = sesiones(request)
    if request.session.get('token_cliente'):
        x = Fernet(keyToken)
        id_cliente = str(x.decrypt(request.session.get('token_cliente')), 'utf8')
        OrdersList = Pedido.objects.filter(id_cliente=cliente(id_cliente))
        print(id_cliente, OrdersList)
        return render(request, 'OrdersAsClient.html', {'OrdersList': OrdersList,'Sesion': val,'Sesion': val})
    else:
        return redirect('/SignInAsClient')


def DetallePedidio(request, id):
    val = sesiones(request)
    pedido = Pedido.objects.get(id_pedido=id)
    productos = ProductosPedido.objects.filter(id_pedido=id)
    pago = Pago.objects.filter(id_pedido=id).exists()
    data = dict()
    data["pedido"] = pedido
    data["productos"] = productos
    if pago == True:
        pagoDetails = Pago.objects.get(id_pedido=id)
        data["pagoDetails"] = pagoDetails

    if pedido.EstadoPedido == "Rechazado":
        data["rechazo"] = PedidoRechazado.objects.get(id_pedido=id)
    elif pedido.EstadoPedido != "En Espera":
        data["aceptado"] = PedidoAceptado.objects.get(id_pedido=id)

    data["Sesion"] = val
    return render(request, 'DetallePedidio.html', data)


def DetallePedidoCliente(request, id):
    val = sesiones(request)
    pedido = Pedido.objects.get(id_pedido=id)
    productos = ProductosPedido.objects.filter(id_pedido=id)

    return render(request, 'DetallePedidoCliente.html',
                  {"pedido": pedido, "productos": productos,'Sesion': val})


def Carrito(request):
    val = sesiones(request)
    if request.session.get('token_cliente'):
        print("entro")
        return render(request, 'Carrito.html')
    else:
        print("no entro")
        return redirect('/SignInAsClient')


def productsAsClient(request):
    val = sesiones(request)
    ProductoListado = Producto.objects.all()
    return render(request, 'productsAsClient.html', {"producto": ProductoListado,'Sesion': val})
    # productoListado = Producto.objects.all()
    # return render(request, 'productsAsClient.html', {"producto": productoListado})



def SignInAsClient(request):
    val = sesiones(request)
    return render(request, 'SigninAsClient.html')


def SignInAsAdministrator(request):
    val = sesiones(request)
    return render(request, 'SignInAsAdministrator.html')


def ClientPanel(request):
    val = sesiones(request)
    if request.session.get('token_cliente'):
        return render(request, 'ClientPanel.html')
    else:
        return redirect('/SignInAsClient')
    # return render(request, 'ClientPanel.html')


def OrdersAdministrator(request):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        OrdersList = Pedido.objects.all()
        return render(request, 'OrdersAdministrator.html', {'OrdersList': OrdersList,'Sesion': val})
    # OrdersList = Pedido.objects.all()
    # return render(request, 'OrdersAdministrator.html',{'OrdersList': OrdersList})
    else:
        return redirect('/SignInAsAdministrator')


def PedidosSeleccionados(request):
    val = sesiones(request)
    if request.method == 'POST':
        cat = request.POST['cat']
        if cat == "op01":
            OrdersList = Pedido.objects.all()
        elif cat == "op02":
            OrdersList = Pedido.objects.filter(EstadoPedido="En Espera")
        elif cat == "op03":
            OrdersList = Pedido.objects.filter(EstadoPedido="Aceptado sin enviar")
        elif cat == "op04":
            OrdersList = Pedido.objects.filter(EstadoPedido="Aceptado y enviado")
        else:
            OrdersList = Pedido.objects.filter(EstadoPedido="Rechazado")

        return render(request, 'OrdersAdministrator.html', {'OrdersList': OrdersList,'Sesion': val})


def CategoriesAdministrator(request):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        CategoriaListado = Categoria.objects.all()
        return render(request, 'CategoriesAdministrator.html', {"categoria": CategoriaListado,'Sesion': val})

    else:
        return redirect('/SignInAsAdministrator')


def SizesAdministrator(request):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        TallaListado = Talla.objects.all()
        return render(request, 'SizesAdministrator.html', {"talla": TallaListado,'Sesion': val})
    # TallaListado = Talla.objects.all()
    # return render(request, 'SizesAdministrator.html', {"talla": TallaListado})
    else:
        return redirect('/SignInAsAdministrator')


def ModifyProduct(request, id):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        producto = Producto.objects.get(id_producto=id)
        CategoriaListado = Categoria.objects.all()
        TallaDisponibleListado = TallaDisponible.objects.filter(id_producto=id)
        Lista = []
        for i in TallaDisponibleListado:
            Lista.append(i.id_talla.id_talla)
        tallaListado = Talla.objects.exclude(id_talla__in=Lista)
        return render(request, 'ModifyProduct.html',
                      {"producto": producto, "categoria": CategoriaListado, "talla": tallaListado,
                       "tallaDisponibles": TallaDisponibleListado,'Sesion': val})
    else:
        return redirect('/SignInAsAdministrator')


# no funciona
def ViewProduct(request, id):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        producto = Producto.objects.get(id_producto=id)
        CategoriaListado = Categoria.objects.all()
        TallaDisponibleListado = TallaDisponible.objects.filter(id_producto=id)
        Lista = []

        for i in TallaDisponibleListado:
            Lista.append(i.id_talla.id_talla)
        tallaListado = Talla.objects.exclude(id_talla__in=Lista)
        print(TallaDisponibleListado)
        return render(request, 'ViewProduct.html',
                      {"producto": producto, "categoria": CategoriaListado, "talla": tallaListado,
                       "tallaDisponibles": TallaDisponibleListado,'Sesion': val})

    # producto = Producto.objects.get(id_producto=id)
    # CategoriaListado = Categoria.objects.all()
    # TallaDisponibleListado = TallaDisponible.objects.filter(id_producto=id)
    # Lista = []
    # for i in TallaDisponibleListado:
    #     Lista.append(i.id_talla.id_talla)
    # tallaListado = Talla.objects.exclude(id_talla__in=Lista)
    # return render(request, 'PreviewProductAsAdministrator.html',
    #               {"producto": producto, "categoria": CategoriaListado, "talla": tallaListado,
    #                "tallaDisponibles": TallaDisponibleListado})
    elif request.session.get('token_cliente'):
        print("no entro")
    else:
        return redirect('/SignInAsAdministrator')


def ViewProductClient(request, id):
    val = sesiones(request)
    producto = Producto.objects.get(id_producto=id)
    CategoriaListado = Categoria.objects.all()
    TallaDisponibleListado = TallaDisponible.objects.filter(id_producto=id)
    Lista = []
    for i in TallaDisponibleListado:
        Lista.append(i.id_talla.id_talla)
    tallaListado = Talla.objects.exclude(id_talla__in=Lista)
    return render(request, 'PreviewProductAsClient.html',
                  {"producto": producto, "categoria": CategoriaListado, "talla": tallaListado,
                   "tallaDisponibles": TallaDisponibleListado,'Sesion': val})


def ProductsAdministrator(request):
    val = sesiones(request)
    productoListado = Producto.objects.all()
    return render(request, 'ProductsAdministrator.html', {"producto": productoListado,'Sesion': val})


def AddNewProduct(request):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        CategoriaListado = Categoria.objects.all()
        TallaListado = Talla.objects.all()
        return render(request, 'AddNewProduct.html', {"categoria": CategoriaListado, "talla": TallaListado,'Sesion': val})
    # CategoriaListado = Categoria.objects.all()
    # tallaListado = Talla.objects.all()
    # return render(request, 'AddNewProduct.html', {"categoria": CategoriaListado, "talla": tallaListado})

    else:
        return redirect('/SignInAsAdministrator')


def registroPersona(request):
    val = sesiones(request)
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellidoPaterno = request.POST['appP']
        apellidoMaterno = request.POST['appM']
        ciNumero = request.POST['CiN']
        ciExtension = request.POST['CiE']
        ciComplemento = request.POST['ciC']
        celular = request.POST['celular']
        correo = request.POST['correo']
        user = persona(nombre=nombre, apellidoPaterno=apellidoPaterno, apellidoMaterno=apellidoMaterno,
                       ciNumero=ciNumero, ciExtension=ciExtension, ciComplemento=ciComplemento, celular=celular,
                       correo=correo)
        user.save()
        # currentUser = persona(nombre, apellidoPaterno, apellidoMaterno, ciNumero, ciExtension, ciComplemento, celular, correo).publish()
        # currentUser.publish()
        print(user.get_id_persona(), ' funciona')

        # client = cliente(id_persona=persona(23), usuario='user01', contraseña='pass01')
        # client.save()

        response = render(request, 'RegisterClient.html', {'current_id': user.get_id_persona(),'Sesion': val})
        response.set_cookie('id_persona', user.get_id_persona())
        return response
    else:
        return render(request, 'RegisterPerson.html')


def registroCliente(request):
    x = Fernet(keyToken)
    if request.method == 'POST':
        id_persona = request.COOKIES['id_persona']
        usuario = request.POST['user']
        contraseña = request.POST['pass']
        encrypted = x.encrypt(str.encode(str(contraseña)))
        encrypted = encrypted.decode()
        client = cliente(id_persona=persona(id_persona), usuario=usuario, contraseña=encrypted)
        client.save()
        print(keyToken)
        
        response = redirect('/SignInAsClient/')
        return response




def inicioSesionCliente(request):
    
    
    if request.method == 'POST':
        
        x = Fernet(keyToken)
        usuario = request.POST['user']
        contraseña = request.POST['pass']
        verificar = cliente.objects.get(usuario=usuario)
        encrypted_text = x.encrypt(str.encode(str(verificar.get_id_cliente())))
        decrypted_password = str(x.decrypt(str(verificar.get_contraseña())), 'utf8')
        print(decrypted_password)
        try:
            verificar = cliente.objects.get(usuario=usuario)
            encrypted_text = x.encrypt(str.encode(str(verificar.get_id_cliente())))
            usr = verificar.get_usuario()
            pass1 = verificar.get_contraseña()
            
            
            # print('User: ',usr, 'Pass: ', pass1, 'User: ', usuario, 'Pass: ', contraseña)
            if usuario != usr or contraseña != decrypted_password:
                messages.success(request, 'El nombre de usuario o contraseña no es correcto')
                response = redirect('/SignInAsClient/')

                return response
            else:
                dat2 = (verificar.get_id_persona()).get_id_persona()
                dat1 = verificar.get_id_cliente()
                response = redirect('/')
                request.session['token_cliente'] = encrypted_text.decode()

                print(request.session['token_cliente'])
                '''response.session['id_cliente'] = dat1
                response.session['id_persona'] = dat2'''

                # response.set_cookie('id_cliente', dat1)
                # response.set_cookie('id_persona', dat2)
                return response
        except:
            
            messages.success(request, 'Puta la wea aes del orto')
            response = redirect('/SignInAsClient/')
            return response


def inicioSesionAdministrador(request):
    x = Fernet(keyToken)
    if request.method == 'POST':
        usuario = request.POST['user']
        contraseña = request.POST['pass']
        try:
            verificar = administrador.objects.get(usuario=usuario)
            usr = verificar.get_usuario()
            pass1 = verificar.get_contraseña()
            encrypted_text = x.encrypt(str.encode(str(verificar.get_id_administrador())))

            if usr != usuario or contraseña != pass1 or verificar.estado == "Desactivado":
                messages.success(request, 'El nombre de usuario o contraseña no es correcto')
                response = redirect('/SignInAsAdministrator/')
                return response
            else:
                print("datos correctos")
                rol = ''

                if verificar.rol == "SuperAdministrador":
                    rol = 'token_Superadministrador'
                elif verificar.rol == "Administrador":
                    rol = 'token_administrador'

                request.session[rol] = encrypted_text.decode()

                response = redirect('/')
                return response
        except:
            messages.success(request, 'El nombre de usuario o contraseña no es correctosss')
            response = redirect('/SignInAsAdministrator/')
            return response

def registroProducto(request):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        if request.method == 'POST':
            # ParaRegistro de producto:
            nombre = request.POST['nombre']
            material = request.POST['material']
            cat = request.POST['cat']
            color = request.POST['color']
            precio = request.POST['precio']
            desc = request.POST['desc']
            img = request.FILES['img']

            product = Producto(nombre=nombre, descripcion=desc, color=color, precio=float(precio), material=material,
                               img=img, id_categoria=Categoria(cat))
            product.save()
            id_producto = product.get_id_producto()
            # Para Registro de tallas en las que estara disponible el producto:

            catidadTallas = Talla.objects.count()
            Tallas = Talla.objects.all()
            print(catidadTallas)
            print(Tallas[0].id_talla)
            ListaIdTallas = ()
            for i in range(catidadTallas):
                stock = request.POST[str(Tallas[i].id_talla)]
                obj2 = TallaDisponible(stock=stock, id_producto=Producto(id_producto),
                                       id_talla=Talla(Tallas[i].id_talla))
                obj2.save()

            response = redirect('/ProductsAdministrator/')
            return response
    else:
        response = redirect('/SignInAsAdministrator/')
        return response


def registroCategoria(request):
    val = sesiones(request)
    if request.method == 'POST':
        # ParaRegistro de categoria:

        categoria = request.POST['nombre']
        id = request.POST['id']
        if id == '':
            obj = Categoria(categoria=categoria)
            obj.save()
        else:
            obj = Categoria.objects.get(id_categoria=id)
            obj.categoria = categoria
            obj.save()

        response = redirect('/CategoriesAdministrator/')
        return response


def registroTalla(request):
    val = sesiones(request)
    if request.method == 'POST':
        # ParaRegistro de talla:

        talla = request.POST['nombre']
        largoEspalda = request.POST['size1']
        contornoPecho = request.POST['size2']
        contornoCuello = request.POST['size3']
        id = request.POST['id']
        if id == '':
            obj = Talla(talla=talla, largoEspalda=largoEspalda, contornoPecho=contornoPecho,
                        contornoCuello=contornoCuello)
            obj.save()

            productos = Producto.objects.all()

            for i in productos:
                obj2 = TallaDisponible(stock=0, id_producto=Producto(i.id_producto), id_talla=Talla(obj.get_id_talla()))
                obj2.save()

        else:
            obj = Talla.objects.get(id_talla=id)
            if talla != '':
                obj.talla = talla
            if largoEspalda != '':
                obj.largoEspalda = int(largoEspalda)
            if contornoPecho != '':
                obj.contornoPecho = int(contornoPecho)
            if contornoCuello != '':
                obj.contornoCuello = int(contornoCuello)
            obj.save()

        response = redirect('/SizesAdministrator/')
        return response


def registroPedido(request):
    val = sesiones(request)
    if request.method == 'POST':
        # ParaRegistro de pedido:
        Direccion = request.POST['direccion']
        Zona = request.POST['zona']
        dep = request.POST['dep']
        Apartamento = request.POST['apartamento']
        x = Fernet(keyToken)
        idCliente = str(x.decrypt(request.session.get('token_cliente')), 'utf8')
        EstadoPedido = 'En Espera'
        FechaPedido = datetime.now()
        TotalPagar = 0;

        TallasDisp = TallaDisponible.objects.all()
        catidadTallas = TallaDisponible.objects.count()

        listaProductos = []


        for i in range(catidadTallas):
            text = TallasDisp[i].get_id_tallaCART()
            if text in request.COOKIES:
                cantidad = request.COOKIES[text]
                print(text)
                text2 = int(text.replace('id', ''))
                varProd = TallaDisponible.objects.get(id_tallaDisponible=text2)
                precioU = (Producto.objects.get(id_producto=varProd.id_producto.id_producto)).precio
                TotalPagar += float(cantidad) * precioU
                listaProductos.append([text2, cantidad])

        obj = Pedido(TotalPagar=TotalPagar, Direccion=Direccion, Zona=Zona, Apartamento=Apartamento,
                     EstadoPedido=EstadoPedido, FechaPedido=FechaPedido, id_departamento=Departamento(dep),
                     id_cliente=cliente(idCliente))
        obj.save()

        print(listaProductos)

        for i in range(len(listaProductos)):
            b = listaProductos[i][0]
            a = listaProductos[i][1]

            obj2 = ProductosPedido(cantidad=a, id_pedido=obj, id_tallaDisponible=TallaDisponible(b))
            obj2.save()

        print(obj.id_pedido)
        response = redirect('/PaymentDetails01/' + str(obj.id_pedido))

        for i in range(catidadTallas):
            text = TallasDisp[i].get_id_tallaCART()
            if text in request.COOKIES:
                response.delete_cookie(text)

        return response


def registroPago(request, id):
    val = sesiones(request)
    if request.method == 'POST':
        # ParaRegistro de pedido:
        BancoProveniente = request.POST['banco']
        Comprobante = request.FILES['img']
        MetodoPago = 'transferencia'
        FechaPago = datetime.now()

        obj = Pago(Comprobante=Comprobante, BancoProveniente=BancoProveniente, MetodoPago=MetodoPago,
                   FechaPago=FechaPago, id_pedido=Pedido(id))
        obj.save()

        response = redirect('/productsAsClient/')
        return response


def registroPedidoAceptado(request, id):
    val = sesiones(request)
    if request.method == 'POST':
        FechaAceptacion = datetime.now()

        x = Fernet(keyToken)
        if request.session.get('token_administrador'):
            id_administrador = str(x.decrypt(request.session.get('token_administrador')), 'utf8')
        else:
            id_administrador = str(x.decrypt(request.session.get('token_Superadministrador')), 'utf8')

        obj = PedidoAceptado(FechaAceptacion=FechaAceptacion, id_pedido=Pedido(id),
                             id_administrador=administrador(id_administrador))
        obj.save()

        obj = Pedido.objects.get(id_pedido=id)
        obj.EstadoPedido = "Aceptado sin enviar"
        obj.save()

        response = redirect('/OrdersAdministrator/')
        return response


def modificarAcceso(request, id):
    val = sesiones(request)
    if request.method == 'POST':
        Rol = request.POST['rol']
        Estado = request.POST['estado']

        obj = administrador.objects.get(id_administrador=id)
        obj.Rol = Rol
        obj.Estado = Estado
        obj.save()

        response = redirect('/administratorManager/')
        return response


def registroPedidoRechazado(request, id):
    val = sesiones(request)
    if request.method == 'POST':
        FechaRechazo = datetime.now()
        RazonRechazo = request.POST['textRechazo']
        x = Fernet(keyToken)

        if request.session.get('token_administrador'):
            id_administrador = str(x.decrypt(request.session.get('token_administrador')), 'utf8')
        else:
            id_administrador = str(x.decrypt(request.session.get('token_Superadministrador')), 'utf8')

        obj = PedidoRechazado(FechaRechazo=FechaRechazo, RazonRechazo=RazonRechazo, id_pedido=Pedido(id),
                              id_administrador=administrador(id_administrador))
        obj.save()

        obj = Pedido.objects.get(id_pedido=id)
        obj.EstadoPedido = "Rechazado"
        obj.save()

        response = redirect('/OrdersAdministrator/')
        return response


def registroPedidoEnviado(request, id):
    val = sesiones(request)
    if request.method == 'POST':
        FechaEnvio = datetime.now()

        obj = PedidoAceptado.objects.get(id_pedido=id)
        obj.FechaEnvio = FechaEnvio
        obj.save()

        obj = Pedido.objects.get(id_pedido=id)
        obj.EstadoPedido = "Aceptado y enviado"
        obj.save()

        response = redirect('/OrdersAdministrator/')
        return response


def modificarProducto(request):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        if request.method == 'POST':
            # Para Modificacion de producto:
            id_producto = request.POST['id']
            nombre = request.POST['nombre']
            material = request.POST['material']
            cat = request.POST['cat']
            color = request.POST['color']
            precio = request.POST['precio']
            desc = request.POST['desc']

            obj = Producto.objects.get(id_producto=id_producto)
            obj.nombre = nombre
            obj.material = material
            obj.id_categoria = Categoria(cat)
            obj.color = color
            obj.precio = float(precio)
            obj.descripcion = desc

            if request.FILES != {}:
                img = request.FILES['img']
                obj.img = img

            obj.save()

            # Para Modificacion de tallas en las que estara disponible el producto:

            catidadTallas = Talla.objects.count()
            Tallas = Talla.objects.all()

            # Para crear de tallas en las que estara disponible el producto:

            ListaIdTallas = ()
            for i in range(catidadTallas):
                stock = request.POST[str(Tallas[i].id_talla)]
                obj2 = TallaDisponible.objects.get(id_producto=Producto(id_producto),
                                                   id_talla=Talla(Tallas[i].id_talla))
                obj2.stock = int(stock)
                obj2.save()

            response = redirect('/ProductsAdministrator/')
            return response
    else:
        return redirect('/')


def addCart(request, id):
    val = sesiones(request)
    if request.method == 'POST':
        # Para Modificacion de producto:
        Tallas = TallaDisponible.objects.all()
        catidadTallas = TallaDisponible.objects.count()

        response = redirect('/productsAsClient/')
        for i in range(catidadTallas):
            text = Tallas[i].get_id_tallaCART()
            if Tallas[i].stock > 0 and str(Tallas[i].id_producto.id_producto) == id:
                quantity = request.POST[str(text)]
                if int(quantity) > 0:
                    response.set_cookie(text, quantity)

                if str(text) in request.COOKIES and int(quantity) <= 0:
                    response.delete_cookie(str(text))
        return response

def contacts(request):
    val = sesiones(request)
    return render(request, 'contacts.html', {'Sesion': val})

def Carrito(request):
    if request.session.get('token_cliente'):
        val = sesiones(request)
        TallasDisp = TallaDisponible.objects.all()
        catidadTallas = TallaDisponible.objects.count()
        producto = Producto.objects.all()

        TallasDisp = TallaDisponible.objects.all()
        catidadTallas = TallaDisponible.objects.count()
        producto = Producto.objects.all()

        datos = dict()
        listaProductos = []
        subTotal = 0

        for i in range(catidadTallas):
            text = TallasDisp[i].get_id_tallaCART()
            if text in request.COOKIES:
                valor = request.COOKIES[text]
                text2 = int(text.replace('id', ''))
                varProd = TallaDisponible.objects.get(id_tallaDisponible=text2)
                listaProductos.append([Producto.objects.get(id_producto=varProd.id_producto.id_producto), valor,
                                   Talla.objects.get(id_talla=varProd.id_talla.id_talla), ])
                precioU = (Producto.objects.get(id_producto=varProd.id_producto.id_producto)).precio
                subTotal += float(valor) * precioU

            # print(varProd.varProd.)
            # datos[text] = varProd.id_producto
            # lista.append(varProd)

        # producto = Producto.objects.get(id_producto=text)
        # datos['tallas']=lista
        datos['productos'] = [listaProductos]
        datos['Sesion'] = val

        messages.success(request, subTotal)
        return render(request, 'Carrito.html', datos)
    else:
        return redirect('/SignInAsClient/')


def OrderForm(request):
    val = sesiones(request)
    TallasDisp = TallaDisponible.objects.all()
    catidadTallas = TallaDisponible.objects.count()
    producto = Producto.objects.all()

    datos = dict()
    listaProductos = []
    subTotal = 0

    for i in range(catidadTallas):
        text = TallasDisp[i].get_id_tallaCART()
        if text in request.COOKIES:
            valor = request.COOKIES[text]
            text2 = int(text.replace('id', ''))
            varProd = TallaDisponible.objects.get(id_tallaDisponible=text2)
            precioU = (Producto.objects.get(id_producto=varProd.id_producto.id_producto)).precio
            listaProductos.append([Producto.objects.get(id_producto=varProd.id_producto.id_producto), valor,
                                   Talla.objects.get(id_talla=varProd.id_talla.id_talla), float(valor) * precioU])

            subTotal += float(valor) * precioU

            # print(varProd.varProd.)
            # datos[text] = varProd.id_producto
            # lista.append(varProd)

        # producto = Producto.objects.get(id_producto=text)
        # datos['tallas']=lista
    datos['productos'] = [listaProductos]
    datos['departamentos'] = Departamento.objects.all()
    datos['Sesion'] = val

    messages.success(request, subTotal)
    return render(request, 'OrderForm.html', datos)


def ViewProduct(request, id):
    val = sesiones(request)
    if request.session.get('token_administrador') or request.session.get('token_Superadministrador') :
        producto = Producto.objects.get(id_producto=id)
        CategoriaListado = Categoria.objects.all()
        TallaDisponibleListado = TallaDisponible.objects.filter(id_producto=id)
        Lista = []
        for i in TallaDisponibleListado:
            Lista.append(i.id_talla.id_talla)
        tallaListado = Talla.objects.exclude(id_talla__in=Lista)
        return render(request, 'PreviewProductAsAdministrator.html',
                      {"producto": producto, "categoria": CategoriaListado, "talla": tallaListado,
                       "tallaDisponibles": TallaDisponibleListado})
    else:
        return redirect('/SignInAsAdministrator/')


def administratorManager(request):
    val = sesiones(request)
    AdministratorsList = administrador.objects.all()
    return render(request, 'administratorManager.html', {'AdministratorsList': AdministratorsList,'Sesion': val})


def dashboard(request):
    val = sesiones(request)
    data = dict()
    ######################  total ventas general:
    totalVentas = Pedido.objects.filter(EstadoPedido="Aceptado sin enviar").aggregate(Sum("TotalPagar"))
    totalVentas2 = Pedido.objects.filter(EstadoPedido="Aceptado y enviado").aggregate(Sum("TotalPagar"))
    data['TotalVentas'] = totalVentas['TotalPagar__sum'] + totalVentas2['TotalPagar__sum']

    ######################  total ventas ultimo mes:
    fecha = date.today()
    totalVentas = Pedido.objects.filter(EstadoPedido="Aceptado sin enviar", FechaPedido__month=fecha.month).aggregate(
        Sum("TotalPagar"))
    totalVentas2 = Pedido.objects.filter(EstadoPedido="Aceptado y enviado", FechaPedido__month=fecha.month).aggregate(
        Sum("TotalPagar"))
    data['TotalVentasMes'] = totalVentas['TotalPagar__sum'] + totalVentas2['TotalPagar__sum']
    print(data['TotalVentasMes'])

    ######################  total clientes:
    totalClientes = cliente.objects.all().count()
    data['TotalClientes'] = totalClientes
    totalClientesUnPedido = Pedido.objects.filter(EstadoPedido="Aceptado y enviado",
                                                  FechaPedido__month=fecha.month).aggregate(Count("id_cliente"))
    data['totalClientesUnPedido'] = totalClientesUnPedido['id_cliente__count']

    ######################  pedidos recibidos:
    totalPedidos = Pedido.objects.all().count()
    data['totalPedidos'] = totalPedidos
    totalPedidosMes = Pedido.objects.filter(FechaPedido__month=fecha.month).count()
    data['totalPedidosMes'] = totalPedidosMes

    ######################  pedidos rechazados:
    totalRechazados = Pedido.objects.filter(EstadoPedido="Rechazado").count()
    data['totalRechazados'] = totalRechazados
    totalRechazadosMes = Pedido.objects.filter(EstadoPedido="Rechazado", FechaPedido__month=fecha.month).count()
    data['totalRechazadosMes'] = totalRechazadosMes

    ######################  producto menos y maspedido:
    productos = TallaDisponible.objects.all()
    cantidadMax = 0
    cantidadMin = 999999
    objMax = ''
    objMin = ''
    TallaMax = ''
    TallaMin = ''
    for i in productos:
        obj = ProductosPedido.objects.filter(id_tallaDisponible=i.id_tallaDisponible).aggregate(Sum("cantidad"))
        if obj['cantidad__sum'] != None:
            if obj['cantidad__sum'] < cantidadMin:
                cantidadMin = obj['cantidad__sum']
                objMin = i
            if obj['cantidad__sum'] > cantidadMax:
                cantidadMax = obj['cantidad__sum']
                objMax = i
    data['cantidadMax'] = cantidadMax
    data['cantidadMin'] = cantidadMin
    data['objMax'] = objMax
    data['objMin'] = objMin

    departamentos = Departamento.objects.all()

    data['departamentos'] = departamentos

    data['Sesion'] = val

    return render(request, 'dashboard.html', data)


def Logout(request):
    request.session.flush()
    if request.session.session_key is not None:
        request.session.delete()

    return redirect('/')
