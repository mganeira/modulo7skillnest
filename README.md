# 🎓 Sistema de Gestión Académica - Django

## 📋 Descripción del Proyecto

Plataforma web desarrollada en Django para gestionar estudiantes, profesores, cursos e inscripciones de una institución educativa. El sistema implementa relaciones complejas entre entidades con borrado en cascada.

## 🏗️ Arquitectura del Modelo de Datos

### Relaciones Implementadas

```
Profesor (1) ──ForeignKey──> (N) Curso
                                 │
                                 │ ManyToMany (through Inscripcion)
                                 ↓
                            Estudiante (N)
                                 │
                                 │ OneToOneField
                                 ↓
                              Perfil (1)
```

### Modelos Django

#### 1. **Profesor** (Entidad Principal)
- `nombre`: CharField(100)
- `email`: EmailField (único)

#### 2. **Curso** (Relación Muchos a Uno)
- `nombre`: CharField(100)
- `descripcion`: TextField
- `profesor`: ForeignKey → Profesor (CASCADE)
- `estudiantes`: ManyToManyField → Estudiante (through='Inscripcion')

#### 3. **Estudiante** (Entidad Principal)
- `nombre`: CharField(100)
- `email`: EmailField (único)

#### 4. **Inscripcion** (Tabla Intermedia - Muchos a Muchos)
- `estudiante`: ForeignKey → Estudiante (CASCADE)
- `curso`: ForeignKey → Curso (CASCADE)
- `fecha_inscripcion`: DateField (auto)
- `estado`: CharField (choices: 'A'ctivo, 'F'inalizado)
- `nota_final`: FloatField (nullable)
- **Restricción:** `unique_together = ('estudiante', 'curso')`

#### 5. **Perfil** (Relación Uno a Uno)
- `estudiante`: OneToOneField → Estudiante (CASCADE, PK)
- `biografia`: TextField
- `foto`: ImageField
- `redes`: CharField(255)

## 🗄️ Creación Manual de la Base de Datos MySQL

### Paso 1: Preparar la Base de Datos

```sql
-- Conectarse a MySQL
mysql -u root -p

-- Crear la base de datos
CREATE DATABASE gestion_academica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario para Django
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON gestion_academica.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;

USE gestion_academica;
```

### Paso 2: Eliminar Tablas Existentes (Si es necesario)

```sql
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS academico_perfil;
DROP TABLE IF EXISTS academico_inscripcion;
DROP TABLE IF EXISTS academico_curso;
DROP TABLE IF EXISTS academico_estudiante;
DROP TABLE IF EXISTS academico_profesor;
DROP TABLE IF EXISTS django_migrations;
DROP TABLE IF EXISTS django_content_type;
DROP TABLE IF EXISTS django_session;
DROP TABLE IF EXISTS auth_permission;
DROP TABLE IF EXISTS auth_group;
DROP TABLE IF EXISTS auth_group_permissions;
DROP TABLE IF EXISTS auth_user;
DROP TABLE IF EXISTS auth_user_groups;
DROP TABLE IF EXISTS auth_user_user_permissions;
DROP TABLE IF EXISTS django_admin_log;

SET FOREIGN_KEY_CHECKS = 1;
```

### Paso 3: Crear las Tablas con CASCADE

```sql
-- Tabla Profesor
CREATE TABLE academico_profesor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla Curso (con CASCADE hacia Profesor)
CREATE TABLE academico_curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    profesor_id INT NOT NULL,
    FOREIGN KEY (profesor_id) 
        REFERENCES academico_profesor(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla Estudiante
CREATE TABLE academico_estudiante (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla Inscripcion (con CASCADE hacia Estudiante y Curso)
CREATE TABLE academico_inscripcion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    curso_id INT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    estado VARCHAR(1) NOT NULL DEFAULT 'A',
    nota_final FLOAT NULL,
    UNIQUE KEY (estudiante_id, curso_id),
    FOREIGN KEY (estudiante_id) 
        REFERENCES academico_estudiante(id) 
        ON DELETE CASCADE,
    FOREIGN KEY (curso_id) 
        REFERENCES academico_curso(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla Perfil (con CASCADE hacia Estudiante)
CREATE TABLE academico_perfil (
    estudiante_id INT PRIMARY KEY,
    biografia TEXT,
    foto VARCHAR(100),
    redes VARCHAR(255),
    FOREIGN KEY (estudiante_id) 
        REFERENCES academico_estudiante(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Paso 4: Verificar las Foreign Keys

```sql
SHOW CREATE TABLE academico_curso\G
SHOW CREATE TABLE academico_inscripcion\G
SHOW CREATE TABLE academico_perfil\G
```

### Paso 5: Insertar Datos de Prueba

```sql
-- Insertar profesores
INSERT INTO academico_profesor (nombre, email) VALUES
('Dr. Juan Pérez', 'juan.perez@universidad.cl'),
('Dra. María González', 'maria.gonzalez@universidad.cl');

-- Insertar cursos
INSERT INTO academico_curso (nombre, descripcion, profesor_id) VALUES
('Matemáticas I', 'Cálculo diferencial e integral', 1),
('Álgebra Lineal', 'Vectores y matrices', 1),
('Programación Python', 'Fundamentos de Python', 2),
('Base de Datos', 'Modelado y SQL', 2);

-- Insertar estudiantes
INSERT INTO academico_estudiante (nombre, email) VALUES
('Carlos Ramírez', 'carlos@estudiante.cl'),
('Ana Silva', 'ana@estudiante.cl'),
('Luis Torres', 'luis@estudiante.cl');

-- Insertar inscripciones
INSERT INTO academico_inscripcion (estudiante_id, curso_id, fecha_inscripcion, estado, nota_final) VALUES
(1, 1, '2024-03-01', 'F', 6.5),
(1, 3, '2024-03-01', 'A', NULL),
(2, 1, '2024-03-01', 'A', NULL),
(2, 2, '2024-03-01', 'F', 5.8),
(2, 4, '2024-03-01', 'A', NULL),
(3, 2, '2024-03-01', 'A', NULL),
(3, 3, '2024-03-01', 'A', NULL);

-- Insertar perfiles
INSERT INTO academico_perfil (estudiante_id, biografia, redes) VALUES
(1, 'Estudiante de Ingeniería Civil en Informática', '@carlosdev'),
(2, 'Apasionada por las matemáticas y la programación', '@anasilva'),
(3, 'Futuro Data Scientist', '@luistorres');
```

### Paso 6: Probar el CASCADE

```sql
-- Ver cursos del profesor 1
SELECT * FROM academico_curso WHERE profesor_id = 1;

-- Borrar profesor (borrará sus cursos automáticamente)
DELETE FROM academico_profesor WHERE id = 1;

-- Verificar que los cursos se borraron
SELECT * FROM academico_curso;

-- Restaurar datos si es necesario
-- (Volver a ejecutar los INSERT del Paso 5)
```

## ⚙️ Configuración de Django

### settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_academica',
        'USER': 'django_user',
        'PASSWORD': 'tu_password_seguro',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Instalar Dependencias

```bash
pip install mysqlclient
# O alternativamente:
pip install pymysql
```

### Sincronizar con Django

```bash
# Si creaste las tablas manualmente
python manage.py migrate --fake-initial

# O si prefieres que Django las cree
python manage.py makemigrations
python manage.py migrate
```

## 🌐 Funcionalidades del Sistema Web

### Vistas Implementadas

#### Listados (ListView)
- **Profesores:** `/profesores/` - Lista todos los profesores
- **Cursos:** `/cursos/` - Lista todos los cursos con su profesor
- **Estudiantes:** `/estudiantes/` - Lista todos los estudiantes

#### Detalles (DetailView)
- **Profesor:** `/profesor/<id>/` - Muestra cursos que imparte
- **Curso:** `/curso/<id>/` - Muestra profesor y estudiantes inscritos con notas
- **Estudiante:** `/estudiante/<id>/` - Muestra perfil y cursos inscritos

### Características del Template

- ✨ Diseño moderno con Inter font
- 🎨 Gradientes y sombras suaves
- 📱 Responsive (móvil y desktop)
- 🏫 Header con logo institucional
- 🧭 Navegación integrada entre secciones
- 🔗 Enlaces relacionales entre entidades

## 📊 Consultas SQL Útiles

```sql
-- Ver todos los cursos con su profesor
SELECT c.nombre AS curso, p.nombre AS profesor 
FROM academico_curso c 
JOIN academico_profesor p ON c.profesor_id = p.id;

-- Ver inscripciones con estudiantes y cursos
SELECT e.nombre AS estudiante, c.nombre AS curso, i.estado, i.nota_final
FROM academico_inscripcion i
JOIN academico_estudiante e ON i.estudiante_id = e.id
JOIN academico_curso c ON i.curso_id = c.id;

-- Estudiantes con sus perfiles
SELECT e.nombre, p.biografia, p.redes
FROM academico_estudiante e
LEFT JOIN academico_perfil p ON e.id = p.estudiante_id;

-- Cursos por profesor con cantidad de estudiantes
SELECT p.nombre AS profesor, c.nombre AS curso, COUNT(i.id) AS total_estudiantes
FROM academico_profesor p
JOIN academico_curso c ON p.id = c.profesor_id
LEFT JOIN academico_inscripcion i ON c.id = i.curso_id
GROUP BY p.id, c.id;
```

## 🚀 Ejecución del Proyecto

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Acceder a:
# - Aplicación: http://localhost:8000/
# - Admin: http://localhost:8000/admin/
```

## 📝 Notas Importantes

1. **CASCADE funciona así:**
   - Borrar Profesor → Borra sus Cursos → Borra Inscripciones de esos cursos
   - Borrar Estudiante → Borra su Perfil y sus Inscripciones
   - Borrar Curso → Borra sus Inscripciones

2. **`on_delete` solo va en ForeignKey/OneToOneField**, no en el modelo referenciado

3. **La tabla intermedia `Inscripcion`** permite almacenar datos adicionales (fecha, estado, nota)

4. **Usar `related_name`** facilita las consultas inversas (ej: `profesor.cursos.all()`)

## 🤝 Equipo de Desarrollo

- Sistema desarrollado como ejercicio grupal de Django ORM
- Implementa relaciones: 1:N, N:M, 1:1
- Manejo de borrado en cascada y entidades intermedias

---

**Versión:** 1.0  
**Framework:** Django 5.x  
**Base de Datos:** MySQL 8.x  
**Autor:** Mariel Gajardo
