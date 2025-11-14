# SQL y ORM en Django: Conceptos y Ejemplos del Proyecto

## ¿Qué es SQL?

**SQL (Structured Query Language)** es el lenguaje estándar utilizado para comunicarse con bases de datos relacionales. Permite realizar operaciones como:
- Crear tablas y estructuras de datos
- Insertar, actualizar y eliminar registros
- Consultar datos con condiciones complejas
- Definir relaciones entre tablas

**Ejemplo de SQL puro:**
```sql
-- Obtener todos los profesores
SELECT * FROM academico_profesor;

-- Obtener un profesor específico
SELECT * FROM academico_profesor WHERE id = 1;

-- Obtener cursos de un profesor
SELECT * FROM academico_curso WHERE profesor_id = 1;
```

---

## ¿Qué es un ORM?

**ORM (Object-Relational Mapping)** es una técnica de programación que permite interactuar con una base de datos relacional usando objetos de tu lenguaje de programación (en este caso, Python) en lugar de escribir SQL directamente.

Django incluye su propio ORM potente y elegante que:
- Convierte las clases de Python en tablas de base de datos
- Convierte las instancias de clases en filas de la base de datos
- Traduce automáticamente las operaciones de Python a consultas SQL
- Funciona con múltiples motores de bases de datos (SQLite, PostgreSQL, MySQL, etc.)

---

## Ventajas del ORM de Django

1. **Abstracción de la base de datos**: No necesitas preocuparte por diferencias entre motores de bases de datos.
2. **Código más legible**: Escribes Python en lugar de SQL.
3. **Prevención de SQL Injection**: El ORM sanitiza automáticamente las consultas.
4. **Migraciones automáticas**: Django genera automáticamente el SQL para crear y modificar tablas.
5. **Portabilidad**: Puedes cambiar de base de datos sin reescribir código.

---

## Ejemplos del Proyecto: Modelos y Tablas SQL

### 1. Modelo Profesor

**Código Python (models.py):**
```python
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre
```

**SQL equivalente que Django genera:**
```sql
CREATE TABLE "academico_profesor" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nombre" varchar(100) NOT NULL,
    "email" varchar(254) NOT NULL UNIQUE
);
```

---

### 2. Modelo Curso con ForeignKey (Relación Muchos a Uno)

**Código Python (models.py):**
```python
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')
    estudiantes = models.ManyToManyField('Estudiante', through='Inscripcion')

    def __str__(self):
        return self.nombre
```

**SQL equivalente:**

CREATE TABLE "academico_curso" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nombre" varchar(100) NOT NULL,
    "descripcion" text NOT NULL,
    "profesor_id" integer NOT NULL REFERENCES "academico_profesor" ("id") 
        ON DELETE CASCADE
);


**Nota**: `on_delete=models.CASCADE` significa que si se elimina un profesor, todos sus cursos también se eliminarán automáticamente.

---

### 3. Modelo Inscripcion (Tabla Intermedia)

**Código Python (models.py):**

class Inscripcion(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('F', 'Finalizado'),
    ]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    nota_final = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('estudiante', 'curso')

**SQL equivalente:**

CREATE TABLE "academico_inscripcion" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "estudiante_id" integer NOT NULL REFERENCES "academico_estudiante" ("id"),
    "curso_id" integer NOT NULL REFERENCES "academico_curso" ("id"),
    "fecha_inscripcion" date NOT NULL,
    "estado" varchar(1) NOT NULL,
    "nota_final" real NULL,
    UNIQUE ("estudiante_id", "curso_id")
);


### 4. Modelo Perfil (Relación Uno a Uno)

**Código Python (models.py):**

class Perfil(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, primary_key=True)
    biografia = models.TextField(blank=True)
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    redes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Perfil de {self.estudiante.nombre}'


**SQL equivalente:**

CREATE TABLE "academico_perfil" (
    "estudiante_id" integer NOT NULL PRIMARY KEY 
        REFERENCES "academico_estudiante" ("id") ON DELETE CASCADE,
    "biografia" text NOT NULL,
    "foto" varchar(100) NULL,
    "redes" varchar(255) NOT NULL
);


## Operaciones CRUD: ORM vs SQL

### CREATE (Crear registros)

**ORM de Django:**

# Crear un profesor
profesor = Profesor.objects.create(
    nombre='Juan Pérez',
    email='juan.perez@example.com'
)

# O de manera alternativa:
profesor = Profesor(nombre='Juan Pérez', email='juan.perez@example.com')
profesor.save()


**SQL equivalente:**

INSERT INTO academico_profesor (nombre, email) 
VALUES ('Juan Pérez', 'juan.perez@example.com');



### READ (Leer/Consultar registros)

**ORM de Django:**

# Obtener todos los profesores
profesores = Profesor.objects.all()

# Obtener un profesor por ID
profesor = Profesor.objects.get(id=1)

# Filtrar profesores por nombre
profesores = Profesor.objects.filter(nombre__contains='Juan')

# Obtener cursos de un profesor (usando related_name)
cursos = profesor.cursos.all()


**SQL equivalente:**

-- Todos los profesores
SELECT * FROM academico_profesor;

-- Un profesor específico
SELECT * FROM academico_profesor WHERE id = 1;

-- Filtrar por nombre
SELECT * FROM academico_profesor WHERE nombre LIKE '%Juan%';

-- Cursos de un profesor (JOIN)
SELECT * FROM academico_curso WHERE profesor_id = 1;
```

---

### UPDATE (Actualizar registros)

**ORM de Django:**
```python
# Obtener y actualizar un profesor
profesor = Profesor.objects.get(id=1)
profesor.email = 'nuevo.email@example.com'
profesor.save()

# O actualizar directamente múltiples registros
Profesor.objects.filter(nombre='Juan Pérez').update(email='nuevo@example.com')
```

**SQL equivalente:**
```sql
UPDATE academico_profesor 
SET email = 'nuevo.email@example.com' 
WHERE id = 1;
```

---

### DELETE (Eliminar registros)

**ORM de Django:**
```python
# Eliminar un profesor específico
profesor = Profesor.objects.get(id=1)
profesor.delete()  # Esto también eliminará sus cursos por el CASCADE

# O eliminar directamente
Profesor.objects.filter(id=1).delete()
```

**SQL equivalente:**
```sql
DELETE FROM academico_profesor WHERE id = 1;
-- Los cursos se eliminan automáticamente por la constraint CASCADE
```

---

## Consultas Complejas con Relaciones

### Ejemplo 1: Obtener estudiantes inscritos en un curso

**ORM de Django:**
```python
curso = Curso.objects.get(id=1)

# Opción 1: A través de la relación many-to-many
estudiantes = curso.estudiantes.all()

# Opción 2: A través de la tabla intermedia
inscripciones = curso.inscripcion_set.all()
for inscripcion in inscripciones:
    print(f"{inscripcion.estudiante.nombre} - Estado: {inscripcion.get_estado_display()}")
```

**SQL equivalente:**
```sql
-- Obtener estudiantes del curso
SELECT e.* 
FROM academico_estudiante e
INNER JOIN academico_inscripcion i ON e.id = i.estudiante_id
WHERE i.curso_id = 1;

-- Con información de la inscripción
SELECT e.nombre, i.estado, i.nota_final
FROM academico_estudiante e
INNER JOIN academico_inscripcion i ON e.id = i.estudiante_id
WHERE i.curso_id = 1;
```

---

### Ejemplo 2: Obtener todos los cursos de un estudiante

**ORM de Django:**
```python
estudiante = Estudiante.objects.get(id=1)

# A través de la relación inversa
inscripciones = estudiante.inscripcion_set.all()
for inscripcion in inscripciones:
    print(f"Curso: {inscripcion.curso.nombre}, Nota: {inscripcion.nota_final}")

# O directamente los cursos (sin información de inscripción)
cursos = estudiante.curso_set.all()
```

**SQL equivalente:**
```sql
SELECT c.nombre, i.nota_final, i.estado
FROM academico_curso c
INNER JOIN academico_inscripcion i ON c.id = i.curso_id
WHERE i.estudiante_id = 1;
```

---

### Ejemplo 3: Filtros complejos con Q objects

**ORM de Django:**
```python
from django.db.models import Q

# Buscar cursos cuyo nombre contenga "Python" O cuyo profesor sea "Juan"
cursos = Curso.objects.filter(
    Q(nombre__icontains='Python') | Q(profesor__nombre__icontains='Juan')
)

# Buscar estudiantes con nota final mayor a 7 en estado "Finalizado"
inscripciones = Inscripcion.objects.filter(
    nota_final__gt=7,
    estado='F'
)
```

**SQL equivalente:**
```sql
-- Cursos con Python o profesor Juan
SELECT c.* 
FROM academico_curso c
LEFT JOIN academico_profesor p ON c.profesor_id = p.id
WHERE c.nombre LIKE '%Python%' OR p.nombre LIKE '%Juan%';

-- Inscripciones finalizadas con nota > 7
SELECT * FROM academico_inscripcion
WHERE nota_final > 7 AND estado = 'F';
```

---

### Ejemplo 4: Agregaciones y anotaciones

**ORM de Django:**
```python
from django.db.models import Count, Avg

# Contar cuántos cursos tiene cada profesor
profesores = Profesor.objects.annotate(num_cursos=Count('cursos'))
for profesor in profesores:
    print(f"{profesor.nombre}: {profesor.num_cursos} cursos")

# Obtener el promedio de notas de un curso
curso = Curso.objects.get(id=1)
promedio = curso.inscripcion_set.aggregate(Avg('nota_final'))
print(f"Promedio: {promedio['nota_final__avg']}")
```

**SQL equivalente:**
```sql
-- Contar cursos por profesor
SELECT p.nombre, COUNT(c.id) as num_cursos
FROM academico_profesor p
LEFT JOIN academico_curso c ON p.id = c.profesor_id
GROUP BY p.id, p.nombre;

-- Promedio de notas de un curso
SELECT AVG(nota_final) as promedio
FROM academico_inscripcion
WHERE curso_id = 1;
```

---

## Acceso a la Relación Uno a Uno (Perfil)

**ORM de Django:**
```python
estudiante = Estudiante.objects.get(id=1)

# Acceder al perfil (relación uno a uno)
if hasattr(estudiante, 'perfil'):
    print(estudiante.perfil.biografia)
    
# Crear un perfil
perfil = Perfil.objects.create(
    estudiante=estudiante,
    biografia='Apasionado por la tecnología',
    redes='@usuario_twitter'
)
```

**SQL equivalente:**
```sql
-- Obtener perfil del estudiante
SELECT * FROM academico_perfil WHERE estudiante_id = 1;

-- Crear perfil
INSERT INTO academico_perfil (estudiante_id, biografia, redes)
VALUES (1, 'Apasionado por la tecnología', '@usuario_twitter');
```

---

## Optimización de Consultas: select_related y prefetch_related

Uno de los problemas comunes es el **problema N+1**, donde se realizan muchas consultas a la base de datos.

### Problema N+1:

```python
# ❌ MAL: Esto genera 1 consulta + N consultas (una por cada curso)
cursos = Curso.objects.all()
for curso in cursos:
    print(curso.profesor.nombre)  # Cada iteración hace una consulta SQL nueva
```

### Solución con select_related (para ForeignKey y OneToOne):

```python
# ✅ BIEN: Esto genera solo 1 consulta con JOIN
cursos = Curso.objects.select_related('profesor').all()
for curso in cursos:
    print(curso.profesor.nombre)  # No hay consultas adicionales
```

**SQL generado:**
```sql
SELECT c.*, p.* 
FROM academico_curso c
INNER JOIN academico_profesor p ON c.profesor_id = p.id;
```

### Solución con prefetch_related (para ManyToMany y relaciones inversas):

```python
# ✅ BIEN: Esto genera 2 consultas eficientes
cursos = Curso.objects.prefetch_related('inscripcion_set__estudiante').all()
for curso in cursos:
    for inscripcion in curso.inscripcion_set.all():
        print(inscripcion.estudiante.nombre)  # Ya está cargado en memoria
```

---

## Ver las Consultas SQL que Genera Django

Puedes ver exactamente qué SQL genera Django de varias maneras:

### 1. En el shell de Django:
```python
from django.db import connection

# Hacer alguna consulta
profesores = Profesor.objects.all()

# Ver las consultas ejecutadas
print(connection.queries)
```

### 2. Usando el método .query:
```python
queryset = Profesor.objects.filter(nombre__contains='Juan')
print(queryset.query)  # Muestra el SQL generado
```

### 3. Con el Django Debug Toolbar:
Instalando el paquete `django-debug-toolbar` puedes ver todas las consultas SQL en tiempo real en tu navegador.

---

## Conclusión

El **ORM de Django** es una herramienta poderosa que:

✅ **Simplifica** el código: Escribes Python en lugar de SQL.  
✅ **Aumenta la seguridad**: Previene inyecciones SQL automáticamente.  
✅ **Mejora la portabilidad**: Funciona con diferentes bases de datos sin cambios.  
✅ **Facilita el mantenimiento**: El código es más legible y mantenible.  

Sin embargo, es importante entender el SQL subyacente para:
- Optimizar consultas complejas
- Debuggear problemas de rendimiento
- Saber cuándo usar SQL raw cuando sea necesario

En este proyecto de gestión académica, el ORM nos permite manejar relaciones complejas entre profesores, cursos, estudiantes e inscripciones de manera elegante y eficiente, sin escribir una sola línea de SQL directamente.
