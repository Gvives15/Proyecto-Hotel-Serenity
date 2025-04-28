from django import forms
from myapp.models import Pabellon, Habitacion, Reserva, Comentario, Perfil, ImagenHabitacion, Servicios, ImagenPabellon

class PabellonForm(forms.ModelForm):
    class Meta:
        model = Pabellon
        fields = ['nombre', 'descripcion', 'capacidad', 'ubicacion', 'fecha_construccion', 'estado', 'imagen']

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'

    # Si el campo no debería ser obligatorio
    imagen = forms.ImageField(required=False)
    
class ImagenHabitacionForm(forms.ModelForm):
    class Meta:
        model = ImagenHabitacion
        fields = ['imagen']
        
class ImagenPabellonForm(forms.ModelForm):
    class Meta:
        model = ImagenPabellon
        fields = ['imagen']
        

class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = [
            'tipo',
            'capacidad',
            'descripcion',
            'estado',
            'imagen',
        ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ImagenServicioForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = ['imagen']

class PabellonForm(forms.ModelForm):
    class Meta:
        model = Pabellon
        fields = [
            'nombre',
            'descripcion',
            'capacidad',
            'ubicacion',
            'fecha_construccion',
            'servicios',
            'estado',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_construccion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'servicios': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
  
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['usuario', 'habitacion', 'fecha_inicio', 'fecha_fin', 'numero_huespedes', 'comentarios']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['usuario', 'habitacion', 'texto', 'calificacion']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion', 'fecha_nacimiento', 'documento_identidad', 'foto']