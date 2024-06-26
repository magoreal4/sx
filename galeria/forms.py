from django import forms
from .models import Sitio, Imagen, Comentario, UserProfile
from django.utils import timezone

class ImagesForm(forms.ModelForm):
        # Aquí agregas un campo extra para el comentario, este no está vinculado directamente a un modelo
    comentario = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Imagen
        fields = ['sitio', 'fecha_carga', 'comentario']


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ImagesForm, self).__init__(*args, **kwargs)
        self.fields['fecha_carga'].widget = forms.DateInput(attrs={
            'class': 'datepicker',
            'type': 'text',
        })
        self.fields['fecha_carga'].initial = timezone.now().date()
        self.fields['fecha_carga'].disabled = True

        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            sitios = user_profile.sitios.all()
            self.fields['sitio'].queryset = sitios

            # Si sólo hay un sitio, seleccionarlo automáticamente
            if sitios.count() == 1:
                self.fields['sitio'].initial = sitios.first().id
                self.fields['sitio'].disabled = True 
                

class SitioForm(forms.ModelForm):
    class Meta:
        model = Sitio
        fields = ['topografia', 'terreno', 'muro', 'grava_geomembrana', 'porton_acceso', 'spat', 'electrico']
        percentage = forms.IntegerField(widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',
            'max': '100',
            'value': '40',
            'class': 'range range-primary',
            'oninput': "this.nextElementSibling.value = this.value"
        }))