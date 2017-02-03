from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from usuarios.models import Seguidores



class Notificaciones(models.Model):
	tipo = models.IntegerField()
	tipo_id = models.IntegerField()
	user_for = models.IntegerField()
	user = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)
	count = models.BigIntegerField(default=1)
	view = models.BigIntegerField(default=0)
	type_for = models.BigIntegerField()


	def save_notificaciones(type, type_id, uid, n_type_for=0, from_var=0):
		pass


	def save(self, *args, **kwargs):
	    super(Notificaciones, self).save(*args, **kwargs)


	class Meta:
	  	"""docstring for Meta"""
	  	verbose_name = "Notificaciones"
	  	verbose_name_plural = "Notificacioness"
