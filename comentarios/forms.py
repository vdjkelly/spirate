from django import forms

class ComentariosPostsForm(forms.ModelForm):
    # TODO: Define other fields here
    comentarios = forms.CharField(max_length=240, min_length=18, required=True, widget=forms.Textarea(attrs={'class': '', 'id': '', 'placeholder': ''}))
    class Meta:
        model = ComentariosPosts
        fields = ['comentarios']

    def __init__(self, *args, **kwargs):
        super(ComentariosPostsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ComentariosPostsForm, self).clean()
        return cleaned_data
