from django.contrib.auth.models import User
from django.db import models
from posts.models import posts

# Create your models here.

class ComentariosPosts(models.Model):
    user = models.ForeignKey(User)
    posts = models.ForeignKey(posts)
    comentarios = models.TextField()
    def __str__(self):
        return  self.comentario
