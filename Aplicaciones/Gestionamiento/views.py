
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Ubicacion, Proyecto, Presupuesto, Permiso
from django.views.decorators.csrf import csrf_exempt
import os


# Create your views here.

def inicio(request):
    return render(request, "inicio.html")
def plantilla(request):
    return render(request, "plantilla.html")



# Función para mostrar el formulario de nueva ubicación
def nuevaUbicacion(request):
    return render(request, "nuevaUbicacion.html")

# Función para guardar una ubicación
def guardarUbicacion(request):
    if request.method == "POST":
        direccion = request.POST.get("direccion")
        ciudad = request.POST.get("ciudad")
        estado = request.POST.get("estado")
        codigo_postal = request.POST.get("codigo_postal")
        pais = request.POST.get("pais")

        # Validación de campos
        if not direccion or not ciudad or not estado or not codigo_postal or not pais:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("nuevaUbicacion")

        # Guardar en la base de datos
        try:
            ubicacion = Ubicacion.objects.create(
                direccion=direccion,
                ciudad=ciudad,
                estado=estado,
                codigo_postal=codigo_postal,
                pais=pais
            )
            messages.success(request, f"Ubicación '{direccion}' guardada exitosamente.")
            return redirect("listarUbicaciones")  # Redirige a la lista de ubicaciones
        except Exception as e:
            messages.error(request, f"Hubo un error al guardar la ubicación: {str(e)}")
            return redirect("nuevaUbicacion")

# Función para listar todas las ubicaciones
def listarUbicaciones(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, "listarUbicaciones.html", {"ubicaciones": ubicaciones})

# Función para eliminar una ubicación
def eliminarUbicacion(request, id_ubicacion):
    if request.method == "POST":
        try:
            ubicacion = Ubicacion.objects.get(id_ubicacion=id_ubicacion)
            ubicacion.delete()
            return JsonResponse({
                'success': True,
                'message': f"La ubicación {ubicacion.direccion} ha sido eliminada correctamente."
            })
        except Ubicacion.DoesNotExist:
            return JsonResponse({'success': False, 'message': "La ubicación no existe."})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': "Método no permitido."})

# Función para editar una ubicación (cargar formulario)
def editarUbicacion(request, id_ubicacion):
    try:
        ubicacion = Ubicacion.objects.get(id_ubicacion=id_ubicacion)
    except Ubicacion.DoesNotExist:
        messages.error(request, "La ubicación no existe.")
        return redirect('listarUbicaciones')

    return render(request, "editarUbicacion.html", {'ubicacion': ubicacion})

# Función para procesar la edición de una ubicación
def procesarEdicionUbicacion(request, id_ubicacion):
    if request.method == "POST":
        try:
            ubicacion = Ubicacion.objects.get(id_ubicacion=id_ubicacion)
        except Ubicacion.DoesNotExist:
            messages.error(request, "La ubicación no existe.")
            return redirect('listarUbicaciones')

        # Actualizar los valores del objeto
        ubicacion.direccion = request.POST['direccion']
        ubicacion.ciudad = request.POST['ciudad']
        ubicacion.estado = request.POST['estado']
        ubicacion.codigo_postal = request.POST['codigo_postal']
        ubicacion.pais = request.POST['pais']
        
        ubicacion.save()

        messages.success(request, "Ubicación actualizada correctamente.")
        return redirect('listarUbicaciones')

    return redirect('listarUbicaciones')  # Si no es POST, redirigir a la lista

# Función para mostrar proyectos



# 1️⃣ Función para mostrar el formulario de nuevo proyecto
def nuevoProyecto(request):
    ubicaciones = Ubicacion.objects.all()  # Obtener todas las ubicaciones para el formulario
    return render(request, "nuevoProyecto.html", {"ubicaciones": ubicaciones})

# 2️⃣ Función para guardar un nuevo proyecto
def guardarProyecto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        id_ubicacion = request.POST.get("id_ubicacion")

        # Validación de campos
        if not nombre or not descripcion or not fecha_inicio or not id_ubicacion:
            messages.error(request, "Todos los campos obligatorios deben ser completados.")
            return redirect("nuevoProyecto")

        # Guardar en la base de datos
        try:
            ubicacion = Ubicacion.objects.get(id_ubicacion=id_ubicacion)
            Proyecto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin if fecha_fin else None,
                id_ubicacion=ubicacion
            )
            messages.success(request, f"Proyecto '{nombre}' guardado exitosamente.")
            return redirect("listarProyectos")
        except Ubicacion.DoesNotExist:
            messages.error(request, "La ubicación seleccionada no existe.")
            return redirect("nuevoProyecto")

# 3️⃣ Función para listar todos los proyectos
def listarProyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, "listarProyectos.html", {"proyectos": proyectos})

# 4️⃣ Función para eliminar un proyecto
def eliminarProyecto(request, id_proyecto):
    if request.method == "POST":
        try:
            proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
            proyecto.delete()
            return JsonResponse({'success': True, 'message': f"El proyecto '{proyecto.nombre}' ha sido eliminado correctamente."})
        except Proyecto.DoesNotExist:
            return JsonResponse({'success': False, 'message': "El proyecto no existe."})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': "Método no permitido."})

# 5️⃣ Función para editar un proyecto (cargar formulario)
def editarProyecto(request, id_proyecto):
    try:
        proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
        ubicaciones = Ubicacion.objects.all()  # Para el selector de ubicaciones
    except Proyecto.DoesNotExist:
        messages.error(request, "El proyecto no existe.")
        return redirect('listarProyectos')

    return render(request, "editarProyecto.html", {"proyecto": proyecto, "ubicaciones": ubicaciones})

# Función para procesar la edición del proyecto
def procesarEdicionProyecto(request, id_proyecto):
    if request.method == "POST":
        try:
            proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
        except Proyecto.DoesNotExist:
            messages.error(request, "El proyecto no existe.")
            return redirect('listarProyectos')

        # Actualizar los valores del proyecto
        proyecto.nombre = request.POST['nombre']
        proyecto.descripcion = request.POST['descripcion']
        proyecto.fecha_inicio = request.POST['fecha_inicio']
        proyecto.fecha_fin = request.POST['fecha_fin'] if request.POST['fecha_fin'] else None
        proyecto.id_ubicacion = Ubicacion.objects.get(id_ubicacion=request.POST['id_ubicacion'])
        
        proyecto.save()

        messages.success(request, "Proyecto actualizado correctamente.")
        return redirect('listarProyectos')

    return redirect('listarProyectos')  # Si no es POST, redirigir a la lista

# Funciones para presupuesto

# 1️⃣ Función para mostrar el formulario de nuevo presupuesto
def nuevoPresupuesto(request):
    proyectos = Proyecto.objects.all()  # Obtener todos los proyectos para el formulario
    return render(request, "nuevoPresupuesto.html", {"proyectos": proyectos})

# 2️⃣ Función para guardar un nuevo presupuesto
def guardarPresupuesto(request):
    if request.method == "POST":
        id_proyecto = request.POST.get("id_proyecto")
        monto_total = request.POST.get("monto_total")
        monto_utilizado = request.POST.get("monto_utilizado", 0)
        fecha_aprobacion = request.POST.get("fecha_aprobacion")

        # Validación de campos
        if not id_proyecto or not monto_total or not fecha_aprobacion:
            messages.error(request, "Todos los campos obligatorios deben ser completados.")
            return redirect("nuevoPresupuesto")

        # Guardar en la base de datos
        try:
            proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
            Presupuesto.objects.create(
                id_proyecto=proyecto,
                monto_total=monto_total,
                monto_utilizado=monto_utilizado,
                fecha_aprobacion=fecha_aprobacion
            )
            messages.success(request, f"Presupuesto asignado al proyecto '{proyecto.nombre}' guardado exitosamente.")
            return redirect("listarPresupuestos")
        except Proyecto.DoesNotExist:
            messages.error(request, "El proyecto seleccionado no existe.")
            return redirect("nuevoPresupuesto")

# 3️⃣ Función para listar todos los presupuestos
def listarPresupuestos(request):
    presupuestos = Presupuesto.objects.all()
    return render(request, "listarPresupuestos.html", {"presupuestos": presupuestos})

# 4️⃣ Función para eliminar un presupuesto
def eliminarPresupuesto(request, id_presupuesto):
    if request.method == "POST":
        try:
            presupuesto = Presupuesto.objects.get(id_presupuesto=id_presupuesto)
            presupuesto.delete()
            return JsonResponse({'success': True, 'message': f"El presupuesto ID {presupuesto.id_presupuesto} ha sido eliminado correctamente."})
        except Presupuesto.DoesNotExist:
            return JsonResponse({'success': False, 'message': "El presupuesto no existe."})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': "Método no permitido."})

# 5️⃣ Función para editar un presupuesto (cargar formulario)
def editarPresupuesto(request, id_presupuesto):
    try:
        presupuesto = Presupuesto.objects.get(id_presupuesto=id_presupuesto)
        proyectos = Proyecto.objects.all()  # Para el selector de proyectos
    except Presupuesto.DoesNotExist:
        messages.error(request, "El presupuesto no existe.")
        return redirect('listarPresupuestos')

    return render(request, "editarPresupuesto.html", {"presupuesto": presupuesto, "proyectos": proyectos})

# Función para procesar la edición del presupuesto
def procesarEdicionPresupuesto(request, id_presupuesto):
    if request.method == "POST":
        try:
            presupuesto = Presupuesto.objects.get(id_presupuesto=id_presupuesto)
        except Presupuesto.DoesNotExist:
            messages.error(request, "El presupuesto no existe.")
            return redirect('listarPresupuestos')

        # Actualizar los valores del presupuesto
        presupuesto.id_proyecto = Proyecto.objects.get(id_proyecto=request.POST['id_proyecto'])
        presupuesto.monto_total = request.POST['monto_total']
        presupuesto.monto_utilizado = request.POST['monto_utilizado']
        presupuesto.fecha_aprobacion = request.POST['fecha_aprobacion']
        
        presupuesto.save()

        messages.success(request, "Presupuesto actualizado correctamente.")
        return redirect('listarPresupuestos')

    return redirect('listarPresupuestos')  # Si no es POST, redirigir a la lista



# Funciones para permisos

# 1️⃣ Formulario de nuevo permiso
def nuevoPermiso(request):
    proyectos = Proyecto.objects.all()
    return render(request, "nuevoPermiso.html", {"proyectos": proyectos})

# 2️⃣ Guardar un nuevo permiso
def guardarPermiso(request):
    if request.method == "POST":
        id_proyecto = request.POST.get("id_proyecto")
        tipo = request.POST.get("tipo")
        numero_permiso = request.POST.get("numero_permiso")
        fecha_emision = request.POST.get("fecha_emision")
        fecha_vencimiento = request.POST.get("fecha_vencimiento")
        foto = request.FILES.get("foto")

        if not id_proyecto or not tipo or not numero_permiso or not fecha_emision:
            messages.error(request, "Todos los campos obligatorios deben ser completados.")
            return redirect("nuevoPermiso")

        try:
            proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
            permiso = Permiso.objects.create(
                id_proyecto=proyecto,
                tipo=tipo,
                numero_permiso=numero_permiso,
                fecha_emision=fecha_emision,
                fecha_vencimiento=fecha_vencimiento if fecha_vencimiento else None,
                foto=foto
            )
            messages.success(request, f"Permiso '{permiso.tipo}' guardado exitosamente.")
            return redirect("listarPermisos")
        except Proyecto.DoesNotExist:
            messages.error(request, "El proyecto seleccionado no existe.")
            return redirect("nuevoPermiso")
        except Exception as e:
            messages.error(request, f"Error al guardar el permiso: {str(e)}")
            return redirect("nuevoPermiso")

# 3️⃣ Listar permisos
def listarPermisos(request):
    permisos = Permiso.objects.all()
    return render(request, "listarPermisos.html", {"permisos": permisos})

# 4️⃣ Eliminar un permiso
@csrf_exempt
def eliminarPermiso(request, id_permiso):
    if request.method == "POST":
        try:
            permiso = Permiso.objects.get(id_permiso=id_permiso)
            
            # Si el permiso tiene una imagen, eliminarla
            if permiso.foto:
                foto_path = permiso.foto.path
                if os.path.isfile(foto_path):
                    os.remove(foto_path)

            permiso.delete()
            return JsonResponse({'success': True, 'message': f"El permiso '{permiso.tipo}' ha sido eliminado correctamente."})
        except Permiso.DoesNotExist:
            return JsonResponse({'success': False, 'message': "El permiso no existe."})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': "Método no permitido."})

# 5️⃣ Formulario de edición de permiso
def editarPermiso(request, id_permiso):
    try:
        permiso = Permiso.objects.get(id_permiso=id_permiso)
        proyectos = Proyecto.objects.all()
    except Permiso.DoesNotExist:
        messages.error(request, "El permiso no existe.")
        return redirect("listarPermisos")

    return render(request, "editarPermiso.html", {"permiso": permiso, "proyectos": proyectos})

# 6️⃣ Procesar edición de permiso
def procesarEdicionPermiso(request, id_permiso):
    if request.method == "POST":
        try:
            permiso = Permiso.objects.get(id_permiso=id_permiso)
        except Permiso.DoesNotExist:
            messages.error(request, "El permiso no existe.")
            return redirect("listarPermisos")

        permiso.id_proyecto = Proyecto.objects.get(id_proyecto=request.POST['id_proyecto'])
        permiso.tipo = request.POST['tipo']
        permiso.numero_permiso = request.POST['numero_permiso']
        permiso.fecha_emision = request.POST['fecha_emision']
        permiso.fecha_vencimiento = request.POST['fecha_vencimiento'] if request.POST['fecha_vencimiento'] else None

        # Verificar si se subió una nueva foto
        if 'foto' in request.FILES:
            permiso.foto = request.FILES['foto']

        permiso.save()

        messages.success(request, "Permiso actualizado correctamente.")
        return redirect("listarPermisos")

    return redirect("listarPermisos")
