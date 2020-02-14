from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render,redirect
from guru.models import Guru
from mapel.models import KkmMapel,Kelas,Mapel,DescMapel,Mengajar
from raport.models import Raport
from .kkmform import KkmFormset,KkmmapelForm



# Create your views here.

class RaportIndexView(LoginRequiredMixin,ListView):
    model = Raport
    login_url = '/login/'
    template_name = 'raport/index.html'

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