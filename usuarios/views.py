from django.conf import settings
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from usuarios.models import Seguidores
from usuarios.forms import LoginForm
import json
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

"""Login de usuarios """

class NextUrlMixin(object):
    """ Allows to redirect a view to its correct success url. """
    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return reverse_lazy('index_inicio')


class LoginUserFormView(FormView):
    form_class = LoginForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'usuarios/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginUserFormView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginUserFormView, self).form_valid(form)

    """ Si el form es invalido! """
    def form_invalid(self, form):
        self.set_test_cookie()
        return super(LoginUserFormView, self).form_invalid(form)

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        self.set_test_cookie()
        return super(LoginUserFormView, self).get(request, *args, **kwargs)



def salir(request):
    logout(request)
    return HttpResponseRedirect('/')


"""Dejar de Seguir"""

class UnFollowView(View):
    def post(self, request, *args, **kwargs):
        json_data = {}
        #Si es ajax pasamos si no damos un error de permisos
        if request.is_ajax:
            if request.user.is_authenticated():
                try:
                    #Verificamos si el usuario existe por medio de su id unico
                    user = User.objects.get(pk=int(request.POST['type_id']))


                except User.DoesNotExist:
                    json_data = {'message': 'El usuario no existe'}
                    return HttpResponse(json.dumps(json_data),  content_type='application/json')
                else:
                    follow = Seguidores.objects.filter(seguido=int(request.POST['type_id']), seguidor_id=request.user.pk).count()
                    if int(follow) > 0:
                        #Hacemos la consulta de usuarios para borrarlos de la BD
                        unfollow = Seguidores.objects.get(tipo=1, seguido=int(request.POST['type_id']), seguidor_id=request.user.pk)
                        unfollow.delete()
                        json_data = {'message': 'Haz dejado de seguir a este usuario ' + user.username}
                    else:
                        json_data = {'message': 'No est&aacute; en tu lista de seguidores'}
                        
            else:
                json_data = {'message': 'Debes loguearte'}
            return HttpResponse(json.dumps(json_data),  content_type='application/json')
        else:
            raise PermissionError
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UnFollowView, self).dispatch(request, *args, **kwargs)

"""Seguir usuarios"""

class FollowView(View):

    def post(self, request, *args, **kwargs):
        json_data = {}
        if request.is_ajax:
            if request.user.is_authenticated:
                try:
                    user = User.objects.get(pk=int(request.POST['type_id']))
                except User.DoesNotExist:
                    json_data = {'message': 'El usuario no existe'}
                    return HttpResponse(json.dumps(json_data),  content_type='application/json')
                else:
                    follow = Seguidores.objects.filter(seguido=int(request.POST['type_id']), seguidor_id=request.user.pk).count()
                    if int(follow) > 0:
                        json_data = {'message': 'Ya estas siguiendo a este usuario'}
                    elif request.user.pk == int(request.POST['type_id']):
                        json_data = {'message': 'No puedes seguirte a ti mismo'}
                    else:
                        ok_follow = Seguidores.objects.create(tipo=1, seguido=int(request.POST['type_id']), seguidor_id=request.user.pk)
                        json_data = {'message': 'Usuario seguido'}
            else:
                json_data = {'message': 'Debes loguearte'}
            return HttpResponse(json.dumps(json_data),  content_type='application/json')
        else:
            raise PermissionError
