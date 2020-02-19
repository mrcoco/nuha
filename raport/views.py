from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View
from django.shortcuts import render,redirect
from django.db.models import Q
from django.forms.models import inlineformset_factory
from openpyxl import Workbook
from guru.models import Guru
from mapel.models import KkmMapel,Kelas,Mapel,DescMapel,Mengajar
from siswa.models import Kelas as KelasSiswa,Siswa
from raport.models import Raport
from .kkmform import KkmFormset,KkmmapelForm
from .raportform import RaportForm
from .render import Render


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
            'title': 'Rapot siswa'
        }
        return context

class RaportCreateView(CreateView):
    model = Raport
    template_name = 'raport/raport_add.html'
    slug_field = 'mapel'
    slug_url_kwarg = 'mapel'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(RaportCreateView, self).get_context_data(**kwargs)
        kkm = KkmMapel.objects.get(pk=self.kwargs['mapel'])
        kelassiswa = KelasSiswa.objects.filter(Q(kelas_id=kkm.kelas_id) & Q(tahun_id=kkm.tahun_id))
        raportformset = inlineformset_factory(KkmMapel.objects.get(pk=self.kwargs['mapel']),Raport,form=RaportForm,min_num=kelassiswa.count(),fields=['kelas','mapel','siswa','tahun','pengetahuan','keterampilan'],max_num=kelassiswa.count(),extra=0,can_delete=False)
        if self.request.POST:
            context['raport'] = raportformset(self.request.POST,instance=kkm)

        else:
            # init = []
            # for murid in kelassiswa:
            #     siswa = Siswa.objects.get(pk= murid.siswa_id)
            #     tahun = TahunAjaran.objects.get(pk=kkm.tahun_id)
            #     kelas = Kelas.objects.get(pk=kkm.kelas_id)
            #     init.append({'lbkelas': kkm.kelas.nama_kelas,'lbnama': murid.siswa.nama,'lbtahun': kkm.tahun.tahun,'lbmapel': kkm.mapel.mapel.nama_mapel,'kelas': kelas,'siswa': siswa,'mapel': kkm.mapel.id,'tahun': tahun})
            # fromset = raportformset(initial=init)
            context = {
                'mapel': self.kwargs['mapel'],
                'kkm': kkm,
                'siswa': kelassiswa,
                'raport': raportformset()
            }
        return context
    #def form_invalid(self, form):
        #context = self.get_context_data(form=form)
        #return JsonResponse({'status': 'ok', 'data': context['raport']})

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['raport']
        return JsonResponse({'status': 'ok', 'data': formset})
        if formset.is_valid():
            response = super().form_valid(form)

            formset.instance = self.object
            formset.save()
            return JsonResponse({'status':'ok','data': self.object})
        else:
            #return super().form_invalid(formset)
            return JsonResponse({'status': 'ok', 'data': formset})


class RaportDownloadView(View):
    model = Raport
    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-movies.xlsx'.format(
            date=datetime.now().strftime('%Y-%m-%d'),
        )
        kkm = get_kkm(self.kwargs['pk'])
        workbook = Workbook
        worksheet = workbook.active
        #worksheet.title = 'Rekap Nilai'
        columns = ['No','NIS','NAMA PESERTA DIDIK','ANGKA','PREDIKAT','DESKRIPSI','ANGKA','PREDIKAT','DESKRIPSI']
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title
        workbook.save(response)
        return response

class RaportDetailView(ListView):
    model = Raport

class RaportPrintView(View):
    model = Raport
    template_name = 'raport/raport_print.html'

    def get(self,request, pk):
        #context = super(RaportPrintView, self).get_context_data(**kwargs)
        #kkm = KkmMapel.objects.get(pk=self.kwargs['pk'])
        kkm = KkmMapel.objects.get(pk=pk)
        guru = kkm.mapel.guru.nama
        nama_mapel = kkm.mapel.mapel.nama_mapel
        tahun = kkm.tahun.tahun
        kelas = kkm.kelas.nama_kelas
        nilai = kkm.raport_set.all()
        rekap_list = []
        for ni in nilai:
            rekap = {}
            rekap['nis'] = ni.siswa.nis
            rekap['siswa'] = ni.siswa.nama
            rekap['angka_pengetahuan'] = ni.pengetahuan
            rekap['angka_keterampilan'] = ni.keterampilan
            rekap['predikat_pengetahuan'] = get_predikat(kkm.pengetahuan,ni.pengetahuan)
            rekap['predikat_keterampilan'] = get_predikat(kkm.ketrampilan,ni.keterampilan)
            rekap['desc_pengetahuan'] = kkm.descmapel_set.get(predikat=get_predikat(kkm.pengetahuan,ni.pengetahuan)).pengetahuan
            rekap['desc_keterampilan'] = kkm.descmapel_set.get(predikat=get_predikat(kkm.ketrampilan,ni.keterampilan)).ketrampilan
            rekap_list.append(rekap)
        # context['tahun'] = tahun
        # context['kelas'] = kelas
        # context['mypk'] = self.kwargs['pk']
        # context['guru'] = guru
        # context['nama_mapel'] = nama_mapel
        # context['nilai'] = rekap_list
        parrams = {
            'tahun': tahun,
            'kelas': kelas,
            'mypk' : pk,
            'guru' : guru,
            'nama_mapel': nama_mapel,
            'nilai': rekap_list,
            'request': request
        }
        return Render.render('raport/raport_print.html',parrams)

class KkmUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = KkmMapel
    login_url = '/login/'
    success_url = '/raport/kkmmapel/'
    success_raport_url = '/raport/raport/'
    success_message = "%(mapel)s was Updated successfully"
    fields = '__all__'
    def get_context_data(self, **kwargs):
        context = super(KkmUpdateView,self).get_context_data(**kwargs)
        siswa = Siswa.objects.filter(kelas__kelas__kkmmapel=self.kwargs['pk'])
        raportformset = inlineformset_factory(KkmMapel, Raport,
                                              form=RaportForm, min_num=siswa.count(),max_num=siswa.count(),
                                              fields=['mapel', 'siswa', 'pengetahuan',
                                                      'keterampilan'], extra=siswa.count() - 1,
                                              can_delete=False)

        if self.request.POST:
            context['kkm_formset'] = KkmFormset(self.request.POST,instance=self.object)
            context['raport_formset'] = raportformset(self.request.POST,instance=self.object)
        else:
            raport = raportformset(instance=self.object)
            for form in raport:
                form.fields['siswa'].queryset = siswa
            context['title'] =  self.object
            context['mpk'] = self.kwargs['pk']
            context['kkm_formset'] = KkmFormset(instance=self.object)
            context['raport_formset'] = raport
        return context
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['kkm_formset']
        raportset = context['raport_formset']
        if form.is_valid():
            if formset is not None:
                if formset.is_valid():
                    response = super().form_valid(form)
                    formset.instance = self.object
                    formset.save()
                    if raportset.is_valid():
                        raportset.instance = self.object
                        raportset.save()
                        return HttpResponseRedirect('/raport/raport')
                    else:
                        return super().form_invalid(raportset)
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
            kelas = Kelas.objects.filter(mengajar__guru_id=guru.id).distinct()
            form = KkmmapelForm()
            form.fields['mapel'].queryset = Mengajar.objects.filter(guru_id=guru.id)
            form.fields['kelas'].queryset = kelas
            formset = KkmFormset()
            context['kkm_formset'] = formset
            context['form'] = form
            context['mpk'] = self.kwargs
            context['title'] = "Tambah KKM"
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
        jadwal = guru.mengajar_set.all()
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
        jadwal = guru.mengajar_set.all()
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

def get_kkmdes(predikat):
    pass

def get_predikat(kkm, nilai):
    nilaimax = 100
    nilaiKkm = kkm
    interval = (nilaimax - nilaiKkm) / 3
    nilaiA = (nilaimax - interval)
    nilaiB = nilaiA - interval
    nilaiC = nilaiB - interval
    nilaiD = nilaiC - interval
    if nilaiA <= nilai <= nilaimax:
        predikat = "A"
    elif nilaiB <= nilai <= nilaiA:
        predikat = "B"
    elif nilaiC <= nilai <= nilaiB:
        predikat = "C"
    elif nilaiD <= nilai <= nilaiC:
        predikat = "D"
    else:
        predikat = "E"
    return predikat