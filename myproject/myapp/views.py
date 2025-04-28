from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Sum 
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    DeleteView, 
    TemplateView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Habitacion, Reserva, Pabellon
from .forms import ReservaForm, PagoForm


# ======= Vistas de Inicio y Navegación =======
def inicio(request):
    """Renderiza la página principal."""
    return render(request, 'myapp/index.html')


# ======= Habitaciones =======
class HabitacionesView(ListView):
    """
    Lista todas las habitaciones disponibles.
    Permite filtrar por tipo de habitación.
    """
    model = Habitacion
    template_name = 'habitaciones/habitaciones.html'
    context_object_name = 'habitaciones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_habitaciones'] = Habitacion.TIPO_CHOICES
        tipo_id = self.request.GET.get('tipo')
        if tipo_id:
            context['habitaciones'] = context['habitaciones'].filter(tipo=tipo_id)
        
        # Cargar imágenes relacionadas con cada habitación
        for habitacion in context['habitaciones']:
            habitacion.imagenes_list = habitacion.imagenes.all()
        
        return context


class DetalleHabitacionView(DetailView):
    """Muestra los detalles de una habitación específica."""
    model = Habitacion
    template_name = 'habitaciones/detalle_habitacion.html'
    context_object_name = 'habitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imagenes'] = self.object.imagenes.all()
        return context
    
def pabellones(request):
    """Lista todos los pabellones disponibles."""
    pabellones = Pabellon.objects.all()
    return render(request, 'habitaciones/pabellones.html', {'pabellones': pabellones})


def detalle_pabellon(request, pabellon_id):
    """Muestra los detalles de un pabellón específico."""
    pabellon = get_object_or_404(Pabellon, id=pabellon_id)
    habitaciones = Habitacion.objects.filter(pabellon=pabellon)
    return render(request, 'habitaciones/detalle_pabellon.html', {'pabellon': pabellon, 'habitaciones': habitaciones})



# ======= Reservas =======
class ReservarHabitacionView(LoginRequiredMixin, CreateView):
    """
    Permite a un usuario autenticado reservar una habitación.
    Verifica la disponibilidad antes de confirmar la reserva.
    """
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/reservar_habitacion.html'
    success_url = reverse_lazy('mis_reservas')

    def form_valid(self, form):
        habitacion = get_object_or_404(Habitacion, id=self.kwargs['habitacion_id'])
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')

        # Verificar conflictos con otras reservas
        reservas_conflictivas = Reserva.objects.filter(
            habitacion=habitacion,
            fecha_inicio__lt=fecha_fin,
            fecha_fin__gt=fecha_inicio
        )
        if reservas_conflictivas.exists():
            form.add_error(None, 'La habitación ya está reservada en estas fechas.')
            return self.form_invalid(form)

        # Guardar la reserva
        reserva = form.save(commit=False)
        reserva.habitacion = habitacion
        reserva.usuario = self.request.user
        reserva.estado = 'pendiente'
        reserva.save()

        messages.success(self.request, 'Reserva creada con éxito.')
        return super().form_valid(form)


class MisReservasView(LoginRequiredMixin, ListView):
    """Lista las reservas del usuario autenticado."""
    model = Reserva
    template_name = 'reservas/mis_reservas.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)


class CancelarReservaView(LoginRequiredMixin, DeleteView):
    """Permite a un usuario cancelar una de sus reservas."""
    model = Reserva
    template_name = 'reservas/cancelar_reserva.html'
    success_url = reverse_lazy('mis_reservas')

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)


class ResumenReservasView(LoginRequiredMixin, TemplateView):
    """
    Muestra un resumen de las reservas pendientes y calcula el total a pagar.
    """
    template_name = 'reservas/resumen_reservas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservas = Reserva.objects.filter(usuario=self.request.user)
        context['reservas'] = reservas
        context['total_pago'] = reservas.filter(estado='pendiente').aggregate(Sum('precio_total'))['precio_total__sum'] or 0
        return context


# ======= Simulación de Pago =======
class SimularPagoView(View):
    """Permite simular el proceso de pago para una reserva."""
    template_name = 'reservas/pagos/simular_pago.html'
    form_class = PagoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            total_pago = form.cleaned_data['total_pago']
            reserva_id = form.cleaned_data['reserva_id']
            try:
                reserva = Reserva.objects.get(id=reserva_id)
                reserva.precio_total = total_pago
                reserva.estado = 'pagada'
                reserva.save()
                return redirect('pago_exitoso')
            except Reserva.DoesNotExist:
                messages.error(request, 'Reserva no encontrada.')
                return redirect('pago_error')
        return render(request, self.template_name, {'form': form})


class PagoExitosoView(View):
    """Muestra la página de pago exitoso."""
    def get(self, request, *args, **kwargs):
        return render(request, 'reservas/pagos/pago_exitoso.html')
 

class PagoErrorView(View):
    """Muestra la página de error en el pago."""
    def get(self, request, *args, **kwargs):
        return render(request, 'reservas/pagos/pago_error.html')


# ======= Usuarios =======
class RegistroView(CreateView):
    """Permite a los usuarios registrarse en el sistema."""
    form_class = UserCreationForm
    template_name = 'cuenta/registro.html'
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class IniciarSesionView(LoginView):
    """Permite a los usuarios iniciar sesión."""
    template_name = 'cuenta/login.html'
    success_url = reverse_lazy('inicio')


class CerrarSesionView(View):
    """Cierra la sesión del usuario autenticado."""
    def get(self, request):
        logout(request)
        return redirect('inicio')


@login_required
def perfil(request):
    """Muestra la página de perfil del usuario."""
    return render(request, 'cuenta/perfil.html')


@login_required
def editar_perfil(request):
    """Permite editar el perfil del usuario autenticado."""
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'cuenta/editar_perfil.html', {'form': form})


# ======= Otros =======

def buscar(request):
    """Realiza búsquedas de habitaciones por nombre."""
    query = request.GET.get('q')
    resultados = Habitacion.objects.filter(nombre__icontains=query) if query else Habitacion.objects.none()
    return render(request, 'myapp/resultados_busqueda.html', {'resultados': resultados, 'query': query})


def contacto(request):
    """Muestra un formulario de contacto y procesa su envío."""
    if request.method == 'POST':
        messages.success(request, 'Mensaje enviado con éxito.')
        return redirect('inicio')
    return render(request, 'myapp/contacto.html')
