from django.http import HttpResponse
from django.shortcuts import render, redirect
from WearRainbow.models import persona, administrador, Producto, Categoria, Talla, TallaDisponible
from WearRainbow.models import cliente
from django.contrib import messages


def paginaIndex(request):
    return render(request, 'index.html')

def SignInAsClient(request):
    return render(request, 'SigninAsClient.html')

def SignInAsAdministrator(request):
    return render(request, 'SignInAsAdministrator.html')


def ClientPanel(request):
    return render(request, 'ClientPanel.html')

def AdministratorPanel(request):
    return render(request, 'AdministratorPanel.html')

def OrdersAdministrator(request):
    return render(request, 'OrdersAdministrator.html')

def ProductsAdministrator(request):
    productoListado = Producto.objects.all()
    return render(request, 'ProductsAdministrator.html', {"producto": productoListado})

def AddNewProduct(request):
    CategoriaListado = Categoria.objects.all()
    tallaListado = Talla.objects.all()
    return render(request, 'AddNewProduct.html', {"categoria": CategoriaListado, "talla": tallaListado})


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
    if request.method == 'POST':
        usuario = request.POST['user']
        contraseña = request.POST['pass']
        try:
            verificar = cliente.objects.get(usuario=usuario)

            usr = verificar.get_usuario()
            pass1 = verificar.get_contraseña()

            if usuario != usr or contraseña != pass1:
                messages.success(request, 'El nombre de usuario o contraseña no es correcto')
                response = redirect('/SignInAsClient/')
                return response
            else:
                dat2 = (verificar.get_id_persona()).get_id_persona()
                dat1 = verificar.get_id_cliente()

                response = redirect('/ClientPanel/')
                response.set_cookie('id_cliente', dat1)
                response.set_cookie('id_persona', dat2)
                return response
        except:
            messages.success(request, 'El nombre de usuario o contraseña no es correcto')
            response = redirect('/SignInAsClient/')
            return response


def inicioSesionAdministrador(request):
    if request.method == 'POST':
        usuario = request.POST['user']
        contraseña = request.POST['pass']
        try:
            verificar = administrador.objects.get(usuario=usuario)

            print(verificar)

            usr = verificar.get_usuario()
            pass1 = verificar.get_contraseña()


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

                response = redirect('/OrdersAdministrator/')
                response.set_cookie('id_administrador', dat1)
                response.set_cookie('id_persona', dat2)
                return response
        except:
            messages.success(request, 'El nombre de usuario o contraseña no es correcto')
            response = redirect('/SignInAsAdministrator/')
            return response

def registroProducto(request):
    if request.method == 'POST':

        #ParaRegistro de producto:
        nombre = request.POST['nombre']
        material = request.POST['material']
        cat = request.POST['cat']
        color = request.POST['color']
        precio = request.POST['precio']
        desc = request.POST['desc']


        product = Producto( nombre=nombre, descripcion=desc, color=color, precio=float(precio), material=material, img="Enter IMG", id_categoria=Categoria(cat))
        product.save()
        id_producto=product.get_id_producto()
        # Para Registro de tallas en las que estara disponible el producto:


        catidadTallas = Talla.objects.count()
        Tallas = Talla.objects.all()
        print(catidadTallas)
        print(Tallas[0].id_talla)
        ListaIdTallas=()
        for i in range(catidadTallas):
            stock = request.POST[str(Tallas[i].id_talla)]
            obj2 = TallaDisponible(stock=stock, id_producto=Producto(id_producto), id_talla=Talla(Tallas[i].id_talla))
            obj2.save()

        response = redirect('/ProductsAdministrator/')
        return response
