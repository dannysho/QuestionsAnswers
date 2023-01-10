from django import forms
from apps.pregunta.models import Pregunta, Respuesta

class PreguntaForm(forms.ModelForm):

    class Meta:

        model = Pregunta

        fields = { 
            'titulo',
            'detalle_pregunta',
        }

        labels = {
            'titulo': 'Titulo',
            'detalle_pregunta': 'detalle_pregunta',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'detalle_pregunta': forms.Textarea(attrs={'class':'form-control'}),
        }

class RespuestaForm(forms.ModelForm):

    class Meta:

        model = Respuesta

        fields = {
            'correcta',
            'detalle_respuesta',
        }

        labels = {
            'correcta': 'Correcta',
            'detalle_respuesta': 'Detalle Respuesta',
        }

        widgets = {
            'correcta': forms.RadioSelect(),
            'detalle_respuesta': forms.Textarea(attrs={'class':'form-control'}),
        }
