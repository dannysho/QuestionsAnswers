from django.db import models

from apps.usuario.models import Usuario

# Create your models here.
class Pregunta(models.Model):
    titulo = models.TextField(max_length=200)
    detalle_pregunta = models.TextField(max_length=200)
    fecha = models.DateTimeField()
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)     

    def save(self, *args, **kwargs):
        self.titulo = (self.titulo).upper()
        return super(Pregunta, self).save(*args, **kwargs)
    
    #def __str__(self):
    #    return str(self.titulo)

    def get_respuestas(self):
        return self.respuesta_set.all()

class Respuesta(models.Model):
    detalle_respuesta = models.CharField(max_length=200)
    correcta = models.BooleanField(default=False)
    fecha = models.DateTimeField() 
    
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE) 
