from django.forms.models import inlineformset_factory, ModelForm
from django import forms
from raport.models import Raport
from mapel.models import KkmMapel

class RaportForm(ModelForm):
    # siswa = forms.IntegerField(widget=forms.HiddenInput())
    # kelas = forms.IntegerField(widget=forms.HiddenInput())
    # tahun = forms.IntegerField(widget=forms.HiddenInput())
    # lbnama = forms.CharField(label="Nama",widget=forms.TextInput(attrs={'class':'vTextField'}))
    # lbkelas = forms.CharField(label="Kelas",widget=forms.TextInput(attrs={'class':'vTextField'}))
    # lbtahun = forms.CharField(label="Tahun Ajaran",widget=forms.TextInput(attrs={'class':'vTextField'}))
    # lbmapel = forms.CharField(label="Mata Pelajaran",widget=forms.TextInput(attrs={'class':'vTextField'}))
    # pengetahuan = forms.IntegerField()
    # keterampilan = forms.IntegerField()
    class Meta:
        model= Raport
        fields = ['siswa', 'mapel', 'pengetahuan', 'keterampilan']

#RaportFormSet = inlineformset_factory(KkmMapel,form=RaportForm,model=Raport,can_delete=False,extra=10)
#RaportFormSet = inlineformset_factory(KkmMapel,Raport,fields=['mapel','pengetahuan','keterampilan','kelas','siswa','tahun'])
