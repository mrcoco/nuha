from django.forms.models import inlineformset_factory, ModelForm
from mapel.models import KkmMapel,DescMapel

class KkmmapelForm(ModelForm):
    class Meta:
        model = KkmMapel
        fields = ['pengetahuan','ketrampilan','kelas','mapel','tahun']

KkmFormset = inlineformset_factory(KkmMapel,DescMapel,fields=['mapel','pengetahuan','ketrampilan','predikat'],exclude=[],can_delete=False,max_num=4,min_num=4)