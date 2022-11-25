from datetime import datetime
from idlelib import window

from django.http import HttpResponse
from django.shortcuts import render, redirect
from WearRainbow.models import persona, administrador, Producto, Categoria, Talla, TallaDisponible, Departamento, \
    Pedido, ProductosPedido
from WearRainbow.models import cliente
from django.contrib import messages
from cryptography.fernet import Fernet

def paginaIndex(request):
    sesion = request.session.get('id_persona')
    if sesion:
        sesion_activa = True 
    else:
        sesion_activa = False
    return render(request, 'index.html',{'Sesion': sesion_activa})

def PaymentDetails01(request):
    return render(request, 'PaymentDetails01.html')

def PaymentDetails02(request):
    return render(request, 'PaymentDetails02.html')

def PaymentDetails03(request):
    return render(request, 'PaymentDetails03.html')

def OrdersAsClient(request):
    if request.session.get('token_cliente'):
       
        id_cliente = request.COOKIES['id_cliente']
        OrdersList = Pedido.objects.filter(id_cliente=cliente(id_cliente))
        print(id_cliente, OrdersList)
        return render(request, 'OrdersAsClient.html', {'OrdersList': OrdersList})
    else:
        return redirect('/SignInAsClient')


def DetallePedidio(request,id):
    pedido = Pedido.objects.get(id_pedido=id)
    productos = ProductosPedido.objects.filter(id_pedido=id)

    return render(request, 'DetallePedidio.html',
                  {"pedido": pedido, "productos": productos})

def DetallePedidoCliente(request,id):
    pedido = Pedido.objects.get(id_pedido=id)
    productos = ProductosPedido.objects.filter(id_pedido=id)

    return render(request, 'DetallePedidoCliente.html',
                  {"pedido": pedido, "productos": productos})

def Carrito(request):
    if request.session.get('token_cliente'):
        return render(request, 'Carrito.html')
    else:
        return redirect('/SignInAsClient')


def productsAsClient(request):
    if request.session.get('token_cliente'):
        ProductoListado = Producto.objects.all()
        return render(request, 'productsAsClient.html', {"producto": ProductoListado})
    # productoListado = Producto.objects.all()
    # return render(request, 'productsAsClient.html', {"producto": productoListado})
    else:
        return redirect('/SignInAsClient')


def contacts(request):
    return render(request, 'contacts.html')


def SignInAsClient(request):
    return render(request, 'SigninAsClient.html')


def SignInAsAdministrator(request):
    return render(request, 'SignInAsAdministrator.html')


def ClientPanel(request):
    if request.session.get('token_cliente'):
        return render(request, 'ClientPanel.html')
    else:
        return redirect('/SignInAsClient')
    #return render(request, 'ClientPanel.html')


def OrdersAdministrator(request):
    if request.session.get('token_administrador'):
        OrdersList = Pedido.objects.all()
        return render(request, 'OrdersAdministrator.html', {'OrdersList': OrdersList})
    # OrdersList = Pedido.objects.all()
    # return render(request, 'OrdersAdministrator.html',{'OrdersList': OrdersList})
    else:
        return redirect('/SignInAsAdministrator')


def CategoriesAdministrator(request):
    if request.session.get('token_administrador'):
        CategoriaListado = Categoria.objects.all()
        return render(request, 'CategoriesAdministrator.html', {"categoria": CategoriaListado})

    # CategoriaListado = Categoria.objects.all()
    # return render(request, 'CategoriesAdministrator.html', {"categoria": CategoriaListado})
    else:
        return redirect('/SignInAsAdministrator')

def SizesAdministrator(request):
    if request.session.get('token_administrador'):
        TallaListado = Talla.objects.all()
        return render(request, 'SizesAdministrator.html', {"talla": TallaListado})
    # TallaListado = Talla.objects.all()
    # return render(request, 'SizesAdministrator.html', {"talla": TallaListado})
    else:
        return redirect('/SignInAsAdministrator')

def ModifyProduct(request, id):
    if request.session.get('token_administrador'):
        producto = Producto.objects.get(id_producto=id)
        CategoriaListado = Categoria.objects.all()
        TallaDisponibleListado = TallaDisponible.objects.filter(id_producto=id)
        Lista = []
        for i in TallaDisponibleListado:
            Lista.append(i.id_talla.id_talla)
        tallaListado = Talla.objects.exclude(id_talla__in=Lista)
        return render(request, 'ModifyProduct.html',
                    {"producto": producto, "categoria": CategoriaListado, "talla": tallaListado,
                    "tallaDisponibles": TallaDisponibleListado})
    else:
        return redirect('/SignInAsAdministrator')


def ViewProduct(request, id):
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


def ViewProductClient(request, id):
    producto = Producto.objects.get(id_producto=id)
    CategoriaListado = Categoria.objects.all()
    TallaDisponibleListado = TallaDisponible.objects.filter(id_producto=id)
    Lista = []
    for i in TallaDisponibleListado:
        Lista.append(i.id_talla.id_talla)
    tallaListado = Talla.objects.exclude(id_talla__in=Lista)
    return render(request, 'PreviewProductAsClient.html',
                  {"producto": producto, "categoria": CategoriaListado, "talla": tallaListado,
                   "tallaDisponibles": TallaDisponibleListado})


def ProductsAdministrator(request):
    user = request.COOKIES.get('id_persona')
    if user:

        productoListado = Producto.objects.all()
        return render(request, 'ProductsAdministrator.html', {"producto": productoListado})
    else:
        return redirect('SignInAsAdministrator')


def AddNewProduct(request):
    if request.session.get('token_admin'):
        print(1)
        CategoriaListado = Categoria.objects.all()
        TallaListado = Talla.objects.all()
        response = render(request, 'AddNewProduct.html', {"categoria": CategoriaListado, "talla": TallaListado})
        #return render(request, 'AddNewProduct.html', {"categoria": CategoriaListado, "talla": TallaListado})
    # CategoriaListado = Categoria.objects.all()
    # tallaListado = Talla.objects.all()
    # print(request.user.is_authenticated)
    else:
        response = redirect('SignInAsAdministrator')
    return response


   

   
        
           
    #return render(request, 'AddNewProduct.html', {"categoria": CategoriaListado, "talla": tallaListado})



def registroPersona(request):
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

        response = render(request, 'RegisterClient.html', {'current_id': user.get_id_persona()})
        response.set_cookie('id_persona', user.get_id_persona())
        return response
    else:
        return render(request, 'RegisterPerson.html')


def registroCliente(request):
    if request.method == 'POST':
        id_persona = request.COOKIES['id_persona']
        usuario = request.POST['user']
        contraseña = request.POST['pass']

        client = cliente(id_persona=persona(id_persona), usuario=usuario, contraseña=contraseña)
        client.save()

        response = redirect('/SignInAsClient/')
        return response


def inicioSesionCliente(request):
    key = Fernet.generate_key()
    x = Fernet(key)
    if request.method == 'POST':
        usuario = request.POST['user']
        contraseña = request.POST['pass']
        encrypted_text = x.encrypt(str.encode(usuario))

        try: 
            verificar = cliente.objects.get(usuario=usuario)
            usr = verificar.get_usuario()
            pass1 = verificar.get_contraseña()
            #print('User: ',usr, 'Pass: ', pass1, 'User: ', usuario, 'Pass: ', contraseña)
            if usuario != usr or contraseña != pass1:
                messages.success(request, 'El nombre de usuario o contraseña no es correcto')
                response = redirect('/SignInAsClient/')
                
                return response
            else:
                dat2 = (verificar.get_id_persona()).get_id_persona()
                dat1 = verificar.get_id_cliente()
                response = redirect('/ClientPanel/')
                request.session['token_cliente'] = encrypted_text.decode()
                print(request.session['token_cliente'])
                '''response.session['id_cliente'] = dat1
                response.session['id_persona'] = dat2'''


                response.set_cookie('id_cliente', dat1)
                response.set_cookie('id_persona', dat2)
                return response
        except:
            
            messages.success(request, 'El nombre de usuario o contraseña no es correctos')
            response = redirect('/SignInAsClient/')
            return response


def inicioSesionAdministrador(request):
    key = Fernet.generate_key()
    x = Fernet(key)
    if request.method == 'POST':
        usuario = request.POST['user']
        contraseña = request.POST['pass']
        
        try:
            verificar = administrador.objects.get(usuario=usuario)

            print(verificar)

            usr = verificar.get_usuario()
            pass1 = verificar.get_contraseña()
            encrypted_text = x.encrypt(str.encode(usuario))

            if usuario != usr or contraseña != pass1:
                messages.success(request, 'El nombre de usuario o contraseña no es correcto')
                response = redirect('/SignInAsAdministrator/')
                return response
            else:
                print("datos correctos")
                dat1 = verificar.get_id_administrador()

                print(dat1)

                dat2 = (verificar.get_id_persona()).get_id_persona()
                print(dat2)
                request.session['token_admin'] = encrypted_text.decode()

                response = redirect('/OrdersAdministrator/')
                response.set_cookie('id_administrador', dat1)
                response.set_cookie('id_persona', dat2)
                return response
        except:
            messages.success(request, 'El nombre de usuario o contraseña no es correcto')
            response = redirect('/SignInAsAdministrator/')
            return response


def registroProducto(request):
    if request.session['token_admin']:
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
                obj2 = TallaDisponible(stock=stock, id_producto=Producto(id_producto), id_talla=Talla(Tallas[i].id_talla))
                obj2.save()

            response = redirect('/ProductsAdministrator/')
            return response
    else:
        response = redirect('/SignInAsAdministrator/')
        return response


def registroCategoria(request):
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

def registroPago(request):
    if request.method == 'POST':

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
    if request.method == 'POST':
        # ParaRegistro de pedido:
        Direccion = request.POST['direccion']
        Zona = request.POST['zona']
        dep = request.POST['dep']
        Apartamento = request.POST['apartamento']
        idCliente=request.COOKIES['id_cliente']
        EstadoPedido='En Espera'
        FechaPedido = datetime.now()
        TotalPagar=0;

        TallasDisp = TallaDisponible.objects.all()
        catidadTallas = TallaDisponible.objects.count()

        listaProductos = []

        response = redirect('/PaymentDetails01/')

        for i in range(catidadTallas):
            text = TallasDisp[i].get_id_tallaCART()
            if text in request.COOKIES:
                cantidad = request.COOKIES[text]
                response.delete_cookie(text)
                text2 = int(text.replace('id', ''))
                varProd = TallaDisponible.objects.get(id_tallaDisponible=text2)
                precioU = (Producto.objects.get(id_producto=varProd.id_producto.id_producto)).precio
                TotalPagar += float(cantidad) * precioU
                listaProductos.append([text2, cantidad])

        obj = Pedido(TotalPagar=TotalPagar, Direccion=Direccion, Zona=Zona, Apartamento=Apartamento, EstadoPedido=EstadoPedido, FechaPedido=FechaPedido, id_departamento=Departamento(dep), id_cliente=cliente(idCliente))
        obj.save()

        print(listaProductos)

        for i in range(len(listaProductos)):
            b=listaProductos[i][0]
            a=listaProductos[i][1]

            obj2=ProductosPedido(cantidad=a,id_pedido=obj, id_tallaDisponible=TallaDisponible(b))
            obj2.save()

        return response


def modificarProducto(request):
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
            obj2 = TallaDisponible.objects.get(id_producto=Producto(id_producto), id_talla=Talla(Tallas[i].id_talla))
            obj2.stock = int(stock)
            obj2.save()

        response = redirect('/ProductsAdministrator/')
        return response


def addCart(request, id):
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


def Carrito(request):
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
            listaProductos.append([Producto.objects.get(id_producto=varProd.id_producto.id_producto), valor, Talla.objects.get(id_talla=varProd.id_talla.id_talla),])
            precioU=(Producto.objects.get(id_producto=varProd.id_producto.id_producto)).precio
            subTotal+=float(valor)*precioU

            # print(varProd.varProd.)
            # datos[text] = varProd.id_producto
            # lista.append(varProd)

        # producto = Producto.objects.get(id_producto=text)
        # datos['tallas']=lista
    datos['productos'] = [listaProductos]
    print(subTotal)

    messages.success(request, subTotal)
    return render(request, 'Carrito.html', datos)


def OrderForm(request):
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
            listaProductos.append([Producto.objects.get(id_producto=varProd.id_producto.id_producto), valor, Talla.objects.get(id_talla=varProd.id_talla.id_talla),float(valor)*precioU])

            subTotal+=float(valor)*precioU

            # print(varProd.varProd.)
            # datos[text] = varProd.id_producto
            # lista.append(varProd)

        # producto = Producto.objects.get(id_producto=text)
        # datos['tallas']=lista
    datos['productos'] = [listaProductos]
    datos['departamentos'] = Departamento.objects.all()
    print(subTotal)

    messages.success(request, subTotal)
    return render(request, 'OrderForm.html', datos)


def ViewProduct(request, id):
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

def Logout(request):
    request.session.flush()
    if request.session.session_key is not None:
        request.session.delete()
  
    return redirect('/')