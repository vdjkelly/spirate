# encoding: utf-8
import mimetypes
import re
from django.core.urlresolvers import reverse
from django.conf import settings
# constantes
THUMB = 'thumb'
SINGLE = 'single'
HOME = 'home'

# devolver la url a la imagen
def get_url_by(type, imagen):
    parts = str(imagen).rsplit('.', 1)
    return '%s%s-%s.%s' % ("static/uploads/%s/%s", parts[0], type, parts[1])


# devolver el archivo a la imagen
def get_path_by(type, path):
    parts = path.rsplit('.', 1)
    return '%s-%s.%s' % (parts[0], type, parts[1])


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse('upload-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
    }

