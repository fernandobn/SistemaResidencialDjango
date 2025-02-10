from django.urls import path
from . import views  # Importa todas las vistas desde views.py

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("plantilla/", views.plantilla, name="plantilla"),

    # Rutas para Ubicaciones
    path("nuevaUbicacion/", views.nuevaUbicacion, name="nuevaUbicacion"),
    path("guardarUbicacion/", views.guardarUbicacion, name="guardarUbicacion"),
    path("listarUbicaciones/", views.listarUbicaciones, name="listarUbicaciones"),
    path("eliminarUbicacion/<int:id_ubicacion>/", views.eliminarUbicacion, name="eliminarUbicacion"),
    path("editarUbicacion/<int:id_ubicacion>/", views.editarUbicacion, name="editarUbicacion"),
    path("procesarEdicionUbicacion/<int:id_ubicacion>/", views.procesarEdicionUbicacion, name="procesarEdicionUbicacion"),

    # Rutas para Proyectos
    path('nuevoProyecto/', views.nuevoProyecto, name='nuevoProyecto'),
    path('guardarProyecto/', views.guardarProyecto, name='guardarProyecto'),
    path('listarProyectos/', views.listarProyectos, name='listarProyectos'),
    path('eliminarProyecto/<int:id_proyecto>/', views.eliminarProyecto, name='eliminarProyecto'),
    path('editarProyecto/<int:id_proyecto>/', views.editarProyecto, name='editarProyecto'),
    path('procesarEdicionProyecto/<int:id_proyecto>/', views.procesarEdicionProyecto, name='procesarEdicionProyecto'),

    # Rutas para presupuestos
    path('nuevoPresupuesto/', views.nuevoPresupuesto, name='nuevoPresupuesto'),
    path('guardarPresupuesto/', views.guardarPresupuesto, name='guardarPresupuesto'),
    path('listarPresupuestos/', views.listarPresupuestos, name='listarPresupuestos'),
    path('eliminarPresupuesto/<int:id_presupuesto>/', views.eliminarPresupuesto, name='eliminarPresupuesto'),
    path('editarPresupuesto/<int:id_presupuesto>/', views.editarPresupuesto, name='editarPresupuesto'),
    path('procesarEdicionPresupuesto/<int:id_presupuesto>/', views.procesarEdicionPresupuesto, name='procesarEdicionPresupuesto'),

    # Rutas para Permisos
    path('nuevoPermiso/', views.nuevoPermiso, name='nuevoPermiso'),
    path('guardarPermiso/', views.guardarPermiso, name='guardarPermiso'),
    path('listarPermisos/', views.listarPermisos, name='listarPermisos'),
    path('eliminarPermiso/<int:id_permiso>/', views.eliminarPermiso, name='eliminarPermiso'),
    path('editarPermiso/<int:id_permiso>/', views.editarPermiso, name='editarPermiso'),
    path('procesarEdicionPermiso/<int:id_permiso>/', views.procesarEdicionPermiso, name='procesarEdicionPermiso'),
]
