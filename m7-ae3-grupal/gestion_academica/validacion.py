# Este script se ejecuta en la consola de Django: python manage.py shell
from academico.models import Profesor, Curso, Estudiante, Inscripcion, Perfil
from django.utils import timezone

def run():
    print("--- Iniciando validación de modelos ---")

    # 4.1 Crear profesores y asignarles cursos
    print("\n--- 4.1 Creando profesores y cursos ---")
    profesor1 = Profesor.objects.create(nombre='Juan Pérez', email='juan.perez@example.com')
    profesor2 = Profesor.objects.create(nombre='Ana Gómez', email='ana.gomez@example.com')
    print(f"Profesores creados: {profesor1.nombre}, {profesor2.nombre}")

    curso1 = Curso.objects.create(nombre='Programación en Python', descripcion='Curso introductorio a Python.', profesor=profesor1)
    curso2 = Curso.objects.create(nombre='Bases de Datos con SQL', descripcion='Curso sobre bases de datos relacionales.', profesor=profesor1)
    curso3 = Curso.objects.create(nombre='Desarrollo Web con Django', descripcion='Curso avanzado de Django.', profesor=profesor2)
    print(f"Cursos creados: '{curso1.nombre}', '{curso2.nombre}', '{curso3.nombre}'")
    print(f"Cursos del profesor {profesor1.nombre}: {[c.nombre for c in profesor1.cursos.all()]}")
    print(f"Cursos del profesor {profesor2.nombre}: {[c.nombre for c in profesor2.cursos.all()]}")

    # 4.2 Crear estudiantes e inscribirlos en cursos
    print("\n--- 4.2 Creando estudiantes e inscripciones ---")
    estudiante1 = Estudiante.objects.create(nombre='Carlos Ruiz', email='carlos.ruiz@example.com')
    estudiante2 = Estudiante.objects.create(nombre='Laura Méndez', email='laura.mendez@example.com')
    print(f"Estudiantes creados: {estudiante1.nombre}, {estudiante2.nombre}")

    # Inscribir a Carlos en Python y a Laura en SQL y Django
    inscripcion1 = Inscripcion.objects.create(estudiante=estudiante1, curso=curso1)
    inscripcion2 = Inscripcion.objects.create(estudiante=estudiante2, curso=curso2)
    inscripcion3 = Inscripcion.objects.create(estudiante=estudiante2, curso=curso3)
    print(f"Inscripción creada: {estudiante1.nombre} en '{curso1.nombre}'")
    print(f"Inscripción creada: {estudiante2.nombre} en '{curso2.nombre}'")
    print(f"Inscripción creada: {estudiante2.nombre} en '{curso3.nombre}'")

    print(f"Estudiantes en '{curso1.nombre}': {[i.estudiante.nombre for i in curso1.inscripcion_set.all()]}")
    print(f"Cursos de {estudiante2.nombre}: {[i.curso.nombre for i in estudiante2.inscripcion_set.all()]}")

    # 4.3 Modificar estados de inscripciones y agregar notas
    print("\n--- 4.3 Modificando inscripciones ---")
    inscripcion1.estado = 'F'
    inscripcion1.nota_final = 8.5
    inscripcion1.save()
    print(f"Inscripción de {inscripcion1.estudiante.nombre} en '{inscripcion1.curso.nombre}' actualizada: Estado={inscripcion1.get_estado_display()}, Nota={inscripcion1.nota_final}")

    # 4.4 Crear perfiles para los estudiantes
    print("\n--- 4.4 Creando perfiles de estudiantes ---")
    perfil1 = Perfil.objects.create(estudiante=estudiante1, biografia='Apasionado por la tecnología y el desarrollo de software.')
    perfil2 = Perfil.objects.create(estudiante=estudiante2, biografia='Interesada en el diseño de bases de datos y la gestión de proyectos.')
    print(f"Perfil creado para {perfil1.estudiante.nombre}: {perfil1.biografia}")
    print(f"Perfil creado para {perfil2.estudiante.nombre}: {perfil2.biografia}")
    print(f"Biografía de {estudiante1.nombre} desde el perfil: {estudiante1.perfil.biografia}")

    # 4.5 Comprobar borrado en cascada
    print("\n--- 4.5 Comprobando borrado en cascada ---")
    cursos_profesor1_count = profesor1.cursos.count()
    print(f"El profesor {profesor1.nombre} tiene {cursos_profesor1_count} cursos antes de ser eliminado.")
    print(f"Cursos totales antes de eliminar al profesor: {Curso.objects.count()}")
    profesor1.delete()
    print(f"Profesor {profesor1.nombre} eliminado.")
    print(f"Cursos totales después de eliminar al profesor: {Curso.objects.count()}")
    cursos_restantes = [c.nombre for c in Curso.objects.all()]
    print(f"Cursos restantes: {cursos_restantes}")
    print("La prueba de borrado en cascada ha sido exitosa si los cursos de Juan Pérez fueron eliminados.")

    print("\n--- Validación finalizada ---")

# Para ejecutar este script, abre la consola de Django con `python manage.py shell`
# y luego ejecuta:
# import validacion
# validacion.run()
run()
