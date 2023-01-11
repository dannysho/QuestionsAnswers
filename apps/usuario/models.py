from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombres = models.TextField(max_length=100)
    apellido_paterno = models.TextField(max_length=50)
    apellido_materno = models.TextField(max_length=50)
    dni = models.TextField(max_length=8)   

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.nombres = (self.nombres).upper()
        self.apellido_paterno = (self.apellido_paterno).upper()
        self.apellido_materno = (self.apellido_materno).upper()
        return super(Usuario, self).save(*args, **kwargs)