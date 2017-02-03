import uuid
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
import os
import datetime
from django.utils import timezone

"""
Categorias en el modelo de posts

"""
class categorias(models.Model):
    nombre = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(max_length=180, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(categorias, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

"""
Post de usuarios
"""


class posts(models.Model):
    titulo = models.CharField(max_length=240, unique=True)
    slug = models.SlugField(max_length=240, editable=False)
    cuerpo = models.TextField()
    categoria = models.ForeignKey(categorias, related_name="posts")
    user = models.ForeignKey(User, related_name="posts")
    tags = models.CharField(max_length=180)
    img_file = models.CharField(max_length=240)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    permitir_comentarios = models.BooleanField(default=True)
    shared = models.PositiveIntegerField(default=0)
    favs = models.PositiveIntegerField(default=0)
    comentarios = models.PositiveIntegerField(default=0)
    follows  = models.PositiveIntegerField(default=0)
    puntos = models.PositiveIntegerField(default=0)
    sticky = models.PositiveIntegerField(default=0)
    follow = models.PositiveIntegerField(default=0)
    ip_autor = models.IPAddressField(default=0)
    autoria_link = models.URLField()
    
    class Meta:
        ordering = ["id"]

    """ Aqui hacemos la funcion hace mas de x tiempo para los post :) """
    def hace(self):
        now = timezone.now()
        days = (now - self.creado).days
        seconds = (now - self.creado).seconds

        if days < 0:
            return 'Nunca'

        if days == 0:
            if seconds < 10:
                return 'Hace unos instantes'
            if seconds < 60:
                return 'Hace unos segundos'
            if seconds < 120:
                return 'Hace minutos'
            if  seconds < 3600:
                return 'Hace unos minutos' 
            if seconds < 7200:
                return 'Hace una hora'
            if seconds < 86400:
                return 'Hace horas'

        if days == 1:
            return 'Ayer'
        if days < 5:
            return 'Hace d&iacute;a'
        if days < 8:
            return 'Hace una semana'
        if days < 14:
            return 'Hace Semanas'
        
        if days < 365:
            month = days / 30
            if month == 1:
                return 'Hace un mes'
            else:
                return 'Hace meses'
        years = days / 365

        if years == 1:
            return 'Hace un a&ntilde;o'
        return 'Hace a&ntilde;os atras'

    def author(self):
        return self.user.username

    def related_post(self):
        pass

    def trucante_title(self):
        if len(self.titulo) < 20:
            return self.titulo
        else:
            return self.titulo[:20] + '...'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(posts, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('ver-posts', args=[str(self.id), slugify(self.titulo)])

    def __str__(self):
        return self.titulo

class Puntos(models.Model):
    """docstring for Puntos 43632451"""
    post = models.ForeignKey(posts, related_name="Puntos")
    user = models.ForeignKey(User, related_name="Puntos")
    puntos = models.PositiveIntegerField(default=0)
    time_p = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Puntos, self).save(*args, **kwargs)


class imagen(models.Model):

    def file_upload(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('static/uploads', filename)

    file = models.ImageField(upload_to=file_upload)
    slug = models.SlugField(max_length=50, blank=True)


    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(imagen, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(imagen, self).delete(*args, **kwargs)
