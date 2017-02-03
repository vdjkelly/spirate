from posts.models import posts

__author__ = 'vdjke'
from django import forms

class PostsForms(forms.ModelForm):

    titulo = forms.CharField(max_length=240, min_length=8, required=True,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'name': 'titulo', 'id': 'titulo', 'placeholder': 'Escribe un titulo'}))
    cuerpo = forms.CharField(required=True,
                             widget=forms.Textarea(attrs={
                                 'class': 'form-control',
                                 'name': 'cuerpo',
                                 'id': 'cuerpo',
                                 'placeholder': 'Contenido del posts'}))
    categoria = forms.Select(attrs={'class': 'form-control'})
    tags = forms.CharField(max_length=240, min_length=10, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                 'placeholder': 'Etiquetas separadas por comas (,)', 'id': 'tags'}))
    img_file = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Seleccion un archivo',
                                   'id': 'append-big-btn',
                                   'readonly': '',

                               }))
    permitir_comentarios = forms.BooleanField(required=False,
                                              widget=forms.CheckboxInput(
                                                  attrs={}))

    class Meta:
        model = posts
        fields = {'titulo', 'categoria', 'cuerpo', 'tags', 'permitir_comentarios', 'img_file'}
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'})
        }
