from django.urls import path, reverse_lazy
from . import views
from .views import (ProductoListView, 
                    ProductoDetailView, 
                    ProductoCreateView, 
                    ProductoEditView, 
                    ProductoDeleteView,
                    CustomLoginView,
                    LogoutView,
                    RegistroView)

app_name = 'productos'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacto/', views.contacto, name='contacto'),
    #path('shop/', views.shop, name='shop'),
    path('crear_producto/', ProductoCreateView, name='crear'),
    path('producto_detalle/<int:pk>/', ProductoDetailView, name='detalle'),
    path('<int:pk>/editar/', ProductoEditView, name='editar'),
    path('<int:pk>/eliminar/', ProductoDeleteView, name='delete'),
    path('lista/', ProductoListView, name='lista_productos'),
    path('login/', CustomLoginView, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('productos:index')), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
]
