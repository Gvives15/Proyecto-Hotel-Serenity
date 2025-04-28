from django.shortcuts import render, redirect
from myapp.models import Habitacion, Reserva, ImagenHabitacion
from django.shortcuts import render, redirect, get_object_or_404
from myadmin.forms import HabitacionForm, ReservaForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

# Vista para el dashboard de administración
def dashboard(request):
    # Calcula estadísticas clave
    total_reservas = Reserva.objects.count()  # Total de reservas
    reservas_activas = Reserva.objects.filter(estado='activa').count()  # Reservas activas
    reservas_canceladas = Reserva.objects.filter(estado='cancelada').count()  # Reservas canceladas
    total_habitaciones = Habitacion.objects.count()  # Total de habitaciones

    # Pasa las estadísticas al contexto para renderizar la vista
    context = {
        'total_reservas': total_reservas,
        'reservas_activas': reservas_activas,
        'reservas_canceladas': reservas_canceladas,
        'total_habitaciones': total_habitaciones,
    }
    return render(request, 'myadmin/dashboard.html', context)  # Renderiza la plantilla del dashboard

# Vista para listar todas las reservas
def listar_reservas(request):
    reservas = Reserva.objects.all()  # Obtiene todas las reservas
    return render(request, 'reservas/listar_reservas.html', {'reservas': reservas})  # Renderiza la lista de reservas

# Vista para crear una nueva reserva
def crear_reserva(request):
    if request.method == 'POST':  # Si el formulario fue enviado
        form = ReservaForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda la nueva reserva
            return redirect('lista_reservas')  # Redirige a la lista de reservas
    else:
        form = ReservaForm()  # Si es un GET, muestra un formulario vacío
    return render(request, 'myadmin/crear_reserva.html', {'form': form})  # Renderiza el formulario

# Vista para eliminar una reserva
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)  # Obtiene la reserva a eliminar

    if request.method == 'POST':  # Si se confirma la eliminación
        reserva.delete()  # Elimina la reserva
        messages.success(request, 'Reserva eliminada con éxito.')  # Muestra un mensaje de éxito
        return redirect('listar_reservas')  # Redirige a la lista de reservas

    # Si es un GET, muestra la confirmación de eliminación
    return render(request, 'myadmin/eliminar_reserva.html', {'reserva': reserva})

# Vista para editar una reserva
def editar_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)  # Obtiene la reserva a editar
    if request.method == 'POST':  # Si el formulario fue enviado
        form = ReservaForm(request.POST, instance=reserva)  # Crea el formulario con los datos existentes
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda la reserva editada
            return redirect('lista_reservas')  # Redirige a la lista de reservas
    else:
        form = ReservaForm(instance=reserva)  # Si es un GET, muestra el formulario con los datos existentes
    return render(request, 'myadmin/editar_reserva.html', {'form': form})  # Renderiza el formulario de edición

from myapp.models import Servicios
from myadmin.forms import ServiciosForm, ImagenServicioForm

# Vista para listar todos los servicios
def listar_servicios(request):
    servicios = Servicios.objects.all()  # Obtiene todos los servicios
    return render(request, 'G.instalaciones/servicios/listar_servicios.html', {'servicios': servicios})

# Vista para crear un nuevo servicio
def crear_servicio(request):
    if request.method == 'POST':  # Si el formulario fue enviado
        form = ServiciosForm(request.POST, request.FILES)  # Crea un formulario con los datos enviados
        if form.is_valid():
            form.save() 
            return redirect('listar_servicio')  # Redirige a la lista de servicios
        else: print("form invalid")
    else:
        form = ServiciosForm()
    return render(request, 'G.instalaciones/servicios/crear_servicio.html', {'form': form })  # Renderiza el formulario

# Vista para editar un servicio
def editar_servicio(request, id):
    servicio = get_object_or_404(Servicios, id=id)  # Obtiene el servicio a editar
    if request.method == 'POST':
        form = ServiciosForm(request.POST, request.FILES, instance=servicio)  # Crea el formulario con los datos existentes
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda el servicio editado
            imagenes = request.FILES.getlist('imagenes')
            for imagen in imagenes:
                ImagenHabitacion.objects.create(servicio=servicio, imagen=imagen)  # Crea imágenes nuevas para la habitación
           
            return redirect('listar_servicio')  # Redirige a la lista de servicios
        else: print ("form invalid")
    else:
        form = ServiciosForm(instance=servicio)  # Si es un GET, muestra el formulario con los datos existentes
    return render(request, 'G.instalaciones/servicios/editar_servicio.html', {'form': form})  # Renderiza el formulario de edición

# Vista para eliminar un servicio
import os
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicios, id=id)  # Obtiene el servicio a eliminar

    if request.method == 'POST':  # Si se confirma la eliminación
        # Verificar si el servicio tiene una imagen asociada
        if servicio.imagen:
            # Obtén la ruta completa de la imagen en el sistema de archivos
            imagen_path = servicio.imagen.path
            
            # Eliminar el archivo de la imagen si existe
            if os.path.exists(imagen_path):
                os.remove(imagen_path)
                print(f"Imagen '{imagen_path}' eliminada correctamente.")

        # Elimina el servicio de la base de datos
        servicio.delete()
        
        # Muestra un mensaje de éxito
        messages.success(request, 'Servicio y su imagen eliminados con éxito.')
        
        # Redirige a la lista de servicios
        return redirect('listar_servicio')

    # Si es un GET, muestra la confirmación de eliminación
    return render(request, 'G.instalaciones/servicios/eliminar_servicio.html', {'servicio': servicio})

from myapp.models import Pabellon
from myadmin.forms import PabellonForm

# Vista para listar todos los pabellones
def listar_pabellones(request):
    pabellones = Pabellon.objects.all()  # Obtiene todos los pabellones
    return render(request, 'G.instalaciones/pabellones/listar_pabellones.html', {'pabellones': pabellones})  # Renderiza la lista de pabellones

# Vista para crear un nuevo pabellón
def crear_pabellon(request):
    if request.method == 'POST':  # Si el formulario fue enviado
        form = PabellonForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda el nuevo pabellón
            return redirect('listar_pabellon')  # Redirige a la lista de pabellones
        else: print("no anda form")
    else:
        form = PabellonForm()  # Si es un GET, muestra un formulario vacío
    return render(request, 'G.instalaciones/pabellones/crear_pabellones.html', {'form': form})  # Renderiza el formulario

# Vista para editar un pabellón
def editar_pabellon(request, id):
    pabellon = get_object_or_404(Pabellon, id=id)  # Obtiene el pabellón a editar
    if request.method == 'POST':  # Si el formulario fue enviado
        form = PabellonForm(request.POST, instance=pabellon)  # Crea el formulario con los datos existentes
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda el pabellón editado
            return redirect('listar_pabellon')  # Redirige a la lista de pabellones
    else:
        form = PabellonForm(instance=pabellon)  # Si es un GET, muestra el formulario con los datos existentes
    return render(request, 'G.instalaciones/pabellones/editar_pabellones.html', {'form': form})  # Renderiza el formulario de edición

# Vista para eliminar un pabellón
def eliminar_pabellon(request, id):
    pabellon = get_object_or_404(Pabellon, id=id)  # Obtiene el pabellón a eliminar

    if request.method == 'POST':  # Si se confirma la eliminación
        pabellon.delete()  # Elimina el pabellón
        messages.success(request, 'Pabellón eliminado con éxito.')  # Muestra un mensaje de éxito
        return redirect('listar_pabellon')  # Redirige a la lista de pabellones

    # Si es un GET, muestra la confirmación de eliminación
    return render(request, 'G.instalaciones/pabellones/eliminar_pabellones.html', {'pabellon': pabellon})



# Vista para listar todas las habitaciones
def listar_habitaciones(request):
    habitaciones = Habitacion.objects.all()  # Obtiene todas las habitaciones
    return render(request, 'G.instalaciones/habitaciones/listar_habitaciones.html', {'habitaciones': habitaciones})  # Renderiza la lista de habitaciones

# Vista para crear una nueva habitación
def crear_habitacion(request):
    if request.method == 'POST':  # Si el formulario fue enviado
        form = HabitacionForm(request.POST, request.FILES)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            habitacion = form.save()  # Guarda la nueva habitación
            # Maneja la carga de múltiples imágenes
            imagenes = request.FILES.getlist('imagenes')  # Obtiene todas las imágenes
            for imagen in imagenes:
                ImagenHabitacion.objects.create(habitacion=habitacion, imagen=imagen)  # Crea imágenes para la habitación
            messages.success(request, 'Habitación creada con éxito.')  # Muestra un mensaje de éxito
            return redirect('listar_habitaciones')  # Redirige a la lista de habitaciones
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')  # Muestra errores si el formulario no es válido
            print(f"el error es: {form.errors}")
    else:
        form = HabitacionForm()  # Si es un GET, muestra un formulario vacío
    return render(request, 'G.instalaciones/habitaciones/crear_habitacion.html', {'form': form})  # Renderiza el formulario de creación

# Vista para editar una habitación
def editar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)  # Obtiene la habitación a editar

    if request.method == 'POST':  # Si el formulario fue enviado
        habitacion_form = HabitacionForm(request.POST, request.FILES, instance=habitacion)  # Crea el formulario con los datos existentes
        if habitacion_form.is_valid():  # Si el formulario es válido
            habitacion_form.save()  # Guarda los cambios en la habitación
            # Maneja la carga de nuevas imágenes
            imagenes = request.FILES.getlist('imagenes')
            for imagen in imagenes:
                ImagenHabitacion.objects.create(habitacion=habitacion, imagen=imagen)  # Crea imágenes nuevas para la habitación
            messages.success(request, 'Habitación actualizada con éxito.')  # Muestra un mensaje de éxito
            return redirect('listar_habitaciones')  # Redirige a la lista de habitaciones
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')  # Muestra errores si el formulario no es válido
    else:
        habitacion_form = HabitacionForm(instance=habitacion)  # Si es un GET, muestra el formulario con los datos existentes

    return render(request, 'G.instalaciones/habitaciones/editar_habitacion.html', {'form': habitacion_form, 'habitacion': habitacion})  # Renderiza el formulario de edición

# Vista para eliminar una habitación
def eliminar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)  # Obtiene la habitación a eliminar

    if request.method == 'POST':  # Si se confirma la eliminación
        habitacion.delete()  # Elimina la habitación
        messages.success(request, 'Habitación eliminada con éxito.')  # Muestra un mensaje de éxito
        return redirect('listar_habitaciones')  # Redirige a la lista de habitaciones

    # Si es un GET, muestra la confirmación de eliminación
    return render(request, 'G.instalaciones/habitaciones/eliminar_habitacion.html', {'habitacion': habitacion})

# Vista para eliminar una imagen de habitación
def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(ImagenHabitacion, id=imagen_id)  # Obtiene la imagen a eliminar
    habitacion_id = imagen.habitacion.id  # Obtiene el ID de la habitación asociada

    if request.method == 'POST':  # Si se confirma la eliminación
        imagen.delete()  # Elimina la imagen
        messages.success(request, 'Imagen eliminada con éxito.')  # Muestra un mensaje de éxito
        return redirect('editar_habitacion', habitacion_id=habitacion_id)  # Redirige a la página de edición de la habitación

    # Si es un GET, muestra la confirmación de eliminación
    return render(request, 'myadmin/eliminar_imagen.html', {'imagen': imagen})





# Vista para registrar un nuevo usuario en el área de administración
def registro_myadmin(request):
    if request.method == 'POST':  # Si el formulario fue enviado
        form = UserCreationForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            user = form.save()  # Guarda el nuevo usuario
            login(request, user)  # Inicia sesión con el nuevo usuario
            return redirect('inicio')  # Redirige al inicio
    else:
        form = UserCreationForm()  # Si es un GET, muestra el formulario vacío
    return render(request, 'cuenta_myadmin/registro_myadmin.html', {'form': form})  # Renderiza el formulario de registro

# Vista para iniciar sesión en el área de administración
def iniciar_sesion_myadmin(request):
    if request.method == 'POST':  # Si el formulario fue enviado
        form = AuthenticationForm(data=request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            user = form.get_user()  # Obtiene al usuario autenticado
            login(request, user)  # Inicia sesión
            return redirect('inicio')  # Redirige al inicio
    else:
        form = AuthenticationForm()  # Si es un GET, muestra el formulario vacío
    return render(request, 'cuenta_myadmin/iniciar_sesion_myadmin.html', {'form': form})  # Renderiza el formulario de inicio de sesión

# Vista para cerrar sesión en el área de administración
def cerrar_sesion_myadmin(request):
    logout(request)  # Cierra sesión
    return redirect('iniciar_sesion_myadmin')  # Redirige a la página de inicio de sesión
