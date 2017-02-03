from urllib.request import urlopen
from uuid import uuid4
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from openid.server.server import HTTP_ERROR
from requests import request
from social.exceptions import AuthException

from social.pipeline.partial import partial
from social.pipeline.user import USER_FIELDS
from social.utils import module_member, slugify
from usuarios.models import Perfil


def create_profile(backend, strategy, is_new, details, response, user, *args, **kwargs):
    if backend.name == "facebook" and is_new:

        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        if Perfil.objects.filter(user_id=user.id).exists():
            pass
        else:
            p = Perfil()
            p.user_id = user.id
            p.foto = url
            p.save()
        return kwargs

    if backend.name == "twitter" and is_new:
        print(details)
