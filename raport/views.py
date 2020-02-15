from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse,JsonResponse
from django.views.generic import CreateView, ListView, UpdateView,FormView,View
from django.shortcuts import render,redirect
from django.db.models import Q
from django.forms.models import inlineformset_factory
from guru.models import Guru
from mapel.models import KkmMapel,Kelas,Mapel,DescMapel,Mengajar
from siswa.models import Kelas as KelasSiswa
from raport.models import Raport
from .kkmform import KkmFormset,KkmmapelForm
from .raportform import RaportForm
import json


# Create your views here.

class RaportIndexView(LoginRequiredMixin,ListView):
    model = Raport
    login_url = '/login/'
    template_name = 'raport/raport.html'
    def get_context_data(self, **kwargs):
        guru = get_guru(self.request.user.id)
        jadwal = get_mengajar(guru)
        context = {
            'jadwal': jadwal,
        }
        return context

class RaportCreateView(FormView):
    #model = Raport
    template_name = 'raport/raport_add.html'
    slug_field = 'mapel'
    slug_url_kwarg = 'mapel'

    def get_context_data(self, **kwargs):
        kkm = KkmMapel.objects.get(pk=self.kwargs['mapel'])
        siswa = KelasSiswa.objects.filter(Q(kelas_id=kkm.kelas_id) & Q(tahun_id=kkm.tahun_id))
        RaportFormset = inlineformset_factory(KkmMapel,Raport,form=RaportForm,min_num=siswa.count(),max_num=siswa.count(),extra=0)
        init = []
        for murid in siswa:
            init.append({'kelas': kkm.kelas_id,'siswa': murid.siswa_id,'mapel': kkm.mapel_id,'tahun': kkm.tahun_id})

        #initial=[{'kelas': kkm.kelas_id},{'kelas': kkm.tahun_id},{'kelas': kkm.kelas_id},{'kelas': kkm.kelas_id}]
        #raportformset = RaportFormSet(initial=init)
        fromset = RaportFormset(initial=init)
        #raportformset.extra_forms = len(initial)
        context = {
            'mapel': self.kwargs['mapel'],
            'kkm': kkm,
            'siswa': siswa,
            'raport': fromset
        }
        return context
    def post(self, request, *args, **kwargs):
        context = {

        }
        return context




class RaportEditView(UpdateView):
    model = Raport

class KkmUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = KkmMapel
    login_url = '/login/'
    success_url = '/raport/kkmmapel/'
    success_message = "%(mapel)s was Updated successfully"
    fields = '__all__'
    def get_context_data(self, **kwargs):
        context = super(KkmUpdateView,self).get_context_data(**kwargs)
        if self.request.POST:
            context['kkm_formset'] = KkmFormset(self.request.POST,instance=self.object)
        else:
            context['kkm_formset'] = KkmFormset(instance=self.object)
        return context
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['kkm_formset']
        if form.is_valid():
            if formset is not None:
                if formset.is_valid():
                    response = super().form_valid(form)
                    formset.instance = self.object
                    formset.save()
                    return response
                else:
                    return super().form_invalid(form)
            else:
                return super().form_invalid(formset)
        else:
            return super().form_invalid(form)

class KkmCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = KkmMapel
    login_url = '/login/'
    success_url = '/raport/kkmmapel/'
    success_message = "%(mapel)s was created successfully"
    fields = '__all__'
    def get_context_data(self, **kwargs):
        context = super(KkmCreateView,self).get_context_data(**kwargs)
        if self.request.POST:
            context['kkm_formset'] = KkmFormset(self.request.POST)
        else:
            guru = get_guru(self.request.user.id)
            form = KkmmapelForm()
            form.fields['mapel'].queryset = Mengajar.objects.filter(guru_id=guru.id)
            form.fields['kelas'].queryset = Kelas.objects.filter(mengajar__guru_id=guru.id).distinct()
            formset = KkmFormset()
            context['kkm_formset'] = formset
            context['form'] = form
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['kkm_formset']
        if form.is_valid():
            if formset is not None:
                if formset.is_valid():
                    response = super().form_valid(form)
                    formset.instance = self.object
                    formset.save()

                    return response
                else:
                    return super().form_invalid(form)
            else:
                return super().form_invalid(formset)
        else:
            return super().form_invalid(form)

class KkmMapelListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    template_name = 'raport/kkmmapel.html'
    model = KkmMapel
    def get_context_data(self, **kwargs):
        guru = get_guru(self.request.user.id)
        jadwal = get_mengajar(guru)
        kkm = KkmMapel.objects.filter(mapel__guru_id=guru.id)
        context = {
            'guru': guru,
            'jadwal': jadwal,
            'kkm': kkm
        }
        return context

class MengajarListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    template_name = 'raport/mengajar.html'
    model = Mengajar
    def get_context_data(self, **kwargs):
        guru = get_guru(self.request.user.id)
        jadwal = get_mengajar(guru)
        context = {
            'guru': guru,
            'jadwal': jadwal,
        }
        return context

def create_raport(request,mapel):
    kkm = KkmMapel.objects.get(pk=mapel)
    #kkm = KkmMapel.objects.get(pk=self.kwargs['mapel'])
    siswa = KelasSiswa.objects.filter(Q(kelas_id=kkm.kelas_id) & Q(tahun_id=kkm.tahun_id))
    # initial=[{'kelas': kkm.kelas_id},{'kelas': kkm.tahun_id},{'kelas': kkm.kelas_id},{'kelas': kkm.kelas_id}]
    # raportformset = RaportFormSet(initial=initial)
    # raportformset.extra_forms = len(initial)
    if request.method == 'POST':
        array = request.POST.getlist('pengetahuan[]')

        return JsonResponse({
            'status': 'ok',
            'array': request.POST,
        })
    else:
        context = {
            'mapel': mapel,
            'kkm': kkm,
            'siswa': siswa,
            # 'raport': raportformset
        }
        return render(request, 'raport/raport_add.html', context)

def index(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    context = {

    }
    return render(request,'raport/index.html',context)

def get_login(request):
    if not request.user.is_authenticated:
        return redirect('login')

def get_guru(userid):
    return Guru.objects.get(user=userid)
def get_kkm(id):
    return KkmMapel.objects.filter(mapel_id=id)

def get_mengajar(guru):
    return Mengajar.objects.filter(guru_id=guru.id)