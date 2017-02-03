from django.db import models
from django.contrib.auth.models import User
from Spirate import settings
class Seguidores(models.Model):
    # TODO: Define fields here
    tipo = models.IntegerField()
    seguido = models.IntegerField()
    seguidor = models.ForeignKey(User)
    creado = models.DateTimeField(auto_now_add=True)

    #Buscamos el listado de seguidores del usuario
    def follow_to_user(tipo,tipo_id, f_tipo_id, f_tipo, omite=0):
        context = {}
        context['user_follows'] = Seguidores.objects.filter(seguidor_id=f_tipo_id,tipo=f_tipo).order_by('?')[:50]
        return context

    def save(self, *args, **kwargs):
        super(Seguidores, self).save(*args, **kwargs)

class Perfil(models.Model):
    # TODO: Define fields here
    user = models.OneToOneField(User)
    pais = models.CharField(max_length=2, blank=True)
    sexo = models.CharField(max_length=2, blank=True)
    posts = models.PositiveIntegerField(default=0)
    comentarios = models.PositiveIntegerField(default=0)
    puntos = models.PositiveIntegerField(default=0)
    puntos_dar = models.PositiveIntegerField(default=10)
    seguidores = models.PositiveIntegerField(default=0)
    siguiendo = models.PositiveIntegerField(default=0)
    foto = models.CharField(max_length=240, blank=True)
    update_puntos = models.PositiveIntegerField(default=0)
    fb_user = models.URLField(max_length=180, default=0)
    tw_user = models.CharField(max_length=180, default=0)
    privacidad = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(auto_now_add=True)
    notificaciones = models.CharField(max_length=2000, blank=True)

    def save(self, *arg, **kwargs):
        super(Perfil, self).save(*arg, **kwargs)

    def __str__(self):
        return str(self.user)
