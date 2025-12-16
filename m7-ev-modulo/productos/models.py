# productos/models.py
from django.db import models

"""
Categoría (1)  ──ForeignKey──>  (N) Producto
                                      │
                                      │ ManyToMany
                                      │
                                      ↓
                                 Etiqueta (M)
                                 
                                 
Producto (1)  ──OneToOne──>  DetalleProducto (1)


Caso de uso real: Una categoría (1) agrupa varios productos (N) → los productos (N) 
pueden tener múltiples etiquetas (M) como "nuevo", "oferta", "destacado" → cada 
producto (1) tiene detalles únicos (1) como dimensiones, peso, material.

Ejemplo concreto:
- Categoría "Electrónica" tiene productos: Laptop, Mouse, Teclado
- Producto "Laptop" tiene etiquetas: "nuevo", "oferta", "gaming"
- Producto "Laptop" tiene DetalleProducto: peso=2.5kg, dimensiones=35x25x2cm


Producto (N) - Categoría (1)
Producto (N) - Etiqueta (M)
Producto (1) - DetalleProducto (1)

"""

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    etiquetas = models.ManyToManyField('Etiquetas')
    
    def __str__(self):
        return self.nombre
    
    def metadata(self):
        return {
            'verbose_name': 'Producto',
            'verbose_name_plural': 'Productos'
        }
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    def metadata(self):
        return {
            'verbose_name': 'Categoría',
            'verbose_name_plural': 'Categorías'
        }
    
class Etiquetas(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
    def metadata(self):
        return {
            'verbose_name': 'Etiqueta',
            'verbose_name_plural': 'Etiquetas'
        }

class DetalleProducto(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    dimensiones = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    material = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Detalle de {self.producto.nombre}"
    
    def metadata(self):
        return {
            'verbose_name': 'Detalle de Producto',
            'verbose_name_plural': 'Detalles de Productos'
        }