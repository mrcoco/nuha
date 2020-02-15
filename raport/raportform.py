from django.forms.models import inlineformset_factory, ModelForm
from django import forms
from raport.models import Raport
from mapel.models import KkmMapel

class RaportForm(ModelForm):
    siswa = forms.CharField()
    kelas = forms.CharField()
    tahun = forms.CharField()
    #mapel = forms.CharField()
    pengetahuan = forms.IntegerField()
    keterampilan = forms.IntegerField()
    class Meta:
        model= Raport
        fields = ['siswa', 'kelas', 'mapel', 'tahun','pengetahuan', 'keterampilan']

#RaportFormSet = inlineformset_factory(KkmMapel,form=RaportForm,model=Raport,can_delete=False,extra=10)
#RaportFormSet = inlineformset_factory(KkmMapel,Raport,fields=['mapel','pengetahuan','keterampilan','kelas','siswa','tahun'])
