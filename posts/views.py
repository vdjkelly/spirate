import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from posts.forms import PostsForms
from posts.models import categorias, posts, imagen, Puntos
from usuarios.models import Seguidores
from .response import JSONResponse, response_mimetype
from .serialize import serialize
from django.views.generic.list import MultipleObjectMixin
from django.http.response import Http404
from usuarios.models import Perfil, Seguidores
from notificaciones.models import Notificaciones
import time


""" Listado de posts en el index"""
class PostsListView(ListView):
    #context_object_name = 'post_page'
    model = posts
    paginate_by = 2
    page_kwarg = 'page'
    ordering = '-id'
    template_name = 'posts/lista_posts.html'

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
            print(context)
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }
            if context_object_name is not None:
                context[context_object_name] = queryset
                context.update(kwargs)
        return super(MultipleObjectMixin, self).get_context_data(**context)

class CreatePosts(FormView):
    categoria = categorias.objects.all()
    model = posts
    template_name = "posts/create_form.html"
    form_class = PostsForms

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        add = form.save(commit=False)
        add.user = self.request.user
        add.img_file = self.request.POST['upload_file']
        add.save()
        form.save_m2m()

        haySeguidores = Seguidores.follow_to_user(2, str(add.pk), int(self.request.user.pk) ,1) #Prueba de notificaciones
        for follows in haySeguidores['user_follows']:
            notis = Notificaciones()
            #print(follows.seguidor_id)

            notis.user = follows.seguidor_id
            notis.tipo = 1
            notis.tipo_id = add.pk
            notis.user_for = self.request.user.pk
            notis.type_for = 0
            notis.save()



        redirect_url = reverse('ver-posts', args=[str(add.pk), slugify(self.request.POST['titulo'])])
        return HttpResponseRedirect(redirect_url)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePosts, self).dispatch(*args, **kwargs)

class PostsView(DetailView):
    model = posts
    template_name = "posts/ver-post.html"
    pk_url_kwarg = 'pk'
    slug_url_kwarg = "slug"
    slug_field = "slug"
    context_object_name = "posts_view"


    def get_context_data(self, **kwargs):
            context = super(PostsView, self).get_context_data(**kwargs)
            context['posts'] = posts.objects.filter(slug=self.kwargs['slug'])
            for post in context['posts']:
                """Seguidores si eres usuario del posts y si eres user de la  web dara un Valor Int 1 si lo sigues 0 si no lo haces"""
                if self.request.user.is_authenticated():
                    context['seguido'] = Seguidores.objects.filter(seguido=post.user_id, seguidor_id=self.request.user).count()
                context['tags'] = post.tags.split(',')
                context['post_autor'] = posts.objects.filter(user_id=post.user_id).order_by('?')[:10]
                context['puntos'] = range(1, 11)
               # context['related_post'] = posts.objects.filter(tags=post.tags).order_by('tags', '-creado').distinct()
               # print(context['related_post'])
            return context

class PuntosTemplateView(TemplateView):
    template_name = None
    def post(self, request):
        if self.request.is_ajax:
            try:
                #Existe el post que vamos a puntuar?
                post = posts.objects.get(pk=self.request.POST['post_id'])
            except posts.DoesNotExist:
                #Aqui damos el error 404 de que no existe el post a puntuar
                json_data = {'message': 'El post no existe o fue eliminado'}
                return HttpResponseBadRequest(json.dumps(json_data), status=404, content_type='application/json')
            else:
                if not request.user.is_superuser: #Usuarios comunes
                    user_info = Perfil.objects.get(user_id=request.user.pk)
                    potsPuntuar = Puntos.objects.filter(post_id=post.pk, user_id=request.user.pk)
                    if potsPuntuar.exists():
                        #Si esta damos este error
                        json_data = {'message': 'No es posible puntuar a un mismo post m&aacute;s de una vez.'}
                    elif request.user.pk == int(post.user_id):
                        json_data = {'message': 'No puedes dar puntos a tu propio post.'}
                    elif user_info.puntos_dar < int(self.request.POST['puntos']):
                        json_data = {'message': 'Voto no v&aacute;lido. No puedes dar  ' + str(request.POST['puntos']) + ' puntos, s&oacute;lo te quedan ' + str(user_info.puntos_dar)}
                    elif int(self.request.POST['puntos']) < 0:
                        json_data = {'message': 'Que malo eres ._.'}
                    else:
                        #Sumamos puntos al post
                        post.puntos += int(request.POST['puntos'])
                        post.save()
                        #Restamos puntos al usuario
                        user_info.puntos_dar -= int(request.POST['puntos'])
                        user_info.save()
                        #Guardo los puntos que dio y si quiere dar de nuevo nos de un error de ya puntuo
                        Puntos.objects.create(puntos=self.request.POST['puntos'], post_id=self.request.POST['post_id'], user_id=request.user.pk)
                        #Imprimo el mensaje de que todo esta bien
                        json_data = {'message': 'Puntos agregados.'}
                    return HttpResponseBadRequest(json.dumps(json_data), status=404, content_type='application/json')

                else: #Solo Administrador y SuperUsuarios
                    potsPuntuar = Puntos.objects.filter(post_id=post.pk, user_id=request.user.pk)
                    if potsPuntuar.exists():
                        json_data = {'message': 'No es posible puntuar a un mismo post m&aacute;s de una vez.'}
                    elif request.user.pk == int(post.user_id):
                        json_data = {'message': 'No puedes dar puntos a tu propio post.'}
                    elif int(self.request.POST['puntos']) < 0:
                        json_data = {'message': 'Que malo eres ._.'}
                    else:
                        #Restamos puntos al usuario
                        post.puntos += int(request.POST['puntos'])
                        post.save()

                        Puntos.objects.create(puntos=self.request.POST['puntos'], post_id=self.request.POST['post_id'], user_id=request.user.pk)
                        json_data = {'message': 'Puntos agregados.'}
                    return HttpResponseBadRequest(json.dumps(json_data), content_type='application/json')
        else:
            raise PermissionError



class PostsDetails(TemplateView):
    template_name = None
    def post(self, request):
        if self.request.is_ajax:
            error_dict = {}
            form = PostsForms(request.POST)
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                return HttpResponseBadRequest(json.dumps(e), status=404, content_type='application/json')
            else:
                cuerpo = self.request.POST['cuerpo']
                titulo = self.request.POST['titulo']
                json_data = {}
                json_data = {'message': titulo, 'cuerpo': cuerpo}
                return HttpResponse(json.dumps(json_data),  content_type='application/json')
        else:
            raise PermissionError

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostsDetails, self).dispatch(request, *args, **kwargs)


"""

"""

class ImagenCreateView(CreateView):
    model = imagen
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dump(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')



class BasicPlusVersionCreateView(ImagenCreateView):
    template_name_suffix = '_basicplus_form'



class ImagenDeleteView(DeleteView):
    model = imagen

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
