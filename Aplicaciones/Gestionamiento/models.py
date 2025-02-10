from django.db import models

class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.direccion}, {self.ciudad}, {self.estado}, {self.pais}"

class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    id_ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name="proyectos")

    def __str__(self):
        return self.nombre

class Presupuesto(models.Model):
    id_presupuesto = models.AutoField(primary_key=True)
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="presupuestos")
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    monto_utilizado = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_aprobacion = models.DateField()

    def __str__(self):
        return f"Presupuesto {self.id_presupuesto} - {self.id_proyecto.nombre}"

class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="permisos")
    tipo = models.CharField(max_length=255)
    numero_permiso = models.CharField(max_length=100, unique=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='gestionamiento', null=True, blank=True, verbose_name="Foto del Robot")

    def __str__(self):
        return f"Permiso {self.tipo} - {self.numero_permiso} ({self.id_proyecto.nombre})"
