from django.contrib.auth.models import User

__author__ = 'vdjke'


def associate_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs