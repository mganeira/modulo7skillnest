from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'productos/login.html'
    redirect_authenticated_user = True  # Si ya está logueado, redirige
    
    def get_success_url(self):
        return reverse_lazy('productos:index')  # A donde ir después del login
    
class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = 'productos/registro.html'
    success_url = reverse_lazy('productos:login')  # Redirige al login después del registro
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro'
        return context
    
    def form_valid(self, form):
        # Opcional: Auto-login después del registro
        from django.contrib.auth import login
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
    
# Vistas públicas (sin login requerido)
def index(request):
    return render(request, 'productos/index.html')

def about(request):
    return render(request, 'productos/about.html')

def contacto(request):
    return render(request, 'productos/contacto.html')

def ProductoListView(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

def ProductoDetailView(request, pk):
    producto = get_object_or_404(Producto, pk=pk)  
    return render(request, 'productos/detalle_producto.html', {'producto': producto})   

# Vistas protegidas (requieren login)
@login_required
def ProductoCreateView(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio)
        producto.save()
        return redirect('productos:lista_productos')
    return render(request, 'productos/crear_producto.html') 

@login_required
def ProductoEditView(request, pk):
    producto = get_object_or_404(Producto, pk=pk)  
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.save()
        return redirect('productos:detalle', pk=producto.pk)
    return render(request, 'productos/editar_producto.html', {'producto': producto})

@login_required
def ProductoDeleteView(request, pk):    
    producto = get_object_or_404(Producto, pk=pk)  
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:lista_productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})