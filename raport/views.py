import io
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View
from django.forms.models import inlineformset_factory

from guru.models import Guru
from mapel.models import KkmMapel,Kelas,Mapel,DescMapel,Mengajar
from siswa.models import Kelas as KelasSiswa,Siswa
from raport.models import Raport
from .kkmform import KkmFormset,KkmmapelForm
from .raportform import RaportForm
from .render import Render
import xlsxwriter


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
            'title': 'Nilai siswa'
        }
        return context

class RaportDownloadView(LoginRequiredMixin,View):
    model = Raport

    def get(self,request, pk):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        kkm = KkmMapel.objects.get(pk=pk)
        guru = kkm.mapel.guru.nama
        nama_mapel = kkm.mapel.mapel.nama_mapel
        tahun = kkm.tahun.tahun
        kelas = kkm.kelas.nama_kelas
        nilai = kkm.raport_set.all()
        cell_format = workbook.add_format({'align': 'center','valign': 'vcenter','border': 1})
        cell_format.set_text_wrap()

        worksheet.write('A1', 'Mata Pelajaran')
        worksheet.write('B1', nama_mapel)
        worksheet.write('H1', 'Guru Mata Pelajaran')
        worksheet.write('I1', guru)
        worksheet.write('A2', 'Kelas/Semester')
        worksheet.write('B2', kelas)
        worksheet.write('H2', 'Tahun Pelajaran')
        worksheet.write('H2', tahun)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('F:F', 25)
        worksheet.set_column('I:B', 25)
        worksheet.merge_range('D4:F4','NILAI PENGETAHUAN',cell_format)
        worksheet.merge_range('G4:I4','NILAI KETERAMPILAN',cell_format)
        worksheet.merge_range('A4:A5','No',cell_format)
        worksheet.merge_range('B4:B5','NIS',cell_format)
        worksheet.merge_range('C4:C5','NAMA PESERTA DIDIK',cell_format)
        worksheet.write('D5', 'ANGKA',cell_format)
        worksheet.write('E5', 'PREDIKAT',cell_format)
        worksheet.write('F5', 'DESKRIPSI',cell_format)
        worksheet.write('G5', 'ANGKA',cell_format)
        worksheet.write('H5', 'PREDIKAT',cell_format)
        worksheet.write('I5', 'DESKRIPSI',cell_format)
        row = 5
        num = 1
        for ni in nilai:
            worksheet.write(row, 0, num,cell_format)
            worksheet.write(row, 1, ni.siswa.nis,cell_format)
            worksheet.write(row, 2, ni.siswa.nama,cell_format)
            worksheet.write(row, 3, ni.pengetahuan,cell_format)
            worksheet.write(row, 4, get_predikat(kkm.pengetahuan, ni.pengetahuan),cell_format)
            worksheet.write(row, 5, kkm.descmapel_set.get(predikat=get_predikat(kkm.pengetahuan, ni.pengetahuan)).pengetahuan,cell_format)
            worksheet.write(row, 6, ni.keterampilan,cell_format)
            worksheet.write(row, 7, get_predikat(kkm.ketrampilan, ni.keterampilan),cell_format)
            worksheet.write(row, 8, kkm.descmapel_set.get(predikat=get_predikat(kkm.ketrampilan, ni.keterampilan)).ketrampilan,cell_format)
            row +=1
            num +=1

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'Rekap_nilai.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

class RaportDetailView(LoginRequiredMixin,ListView):
    model = Raport
    def get_context_data(self, **kwargs):
        context = super(RaportDetailView, self).get_context_data(**kwargs)
        kkm = KkmMapel.objects.get(pk=self.kwargs['pk'])
        guru = kkm.mapel.guru.nama
        nama_mapel = kkm.mapel.mapel.nama_mapel
        tahun = kkm.tahun.tahun
        kelas = kkm.kelas.nama_kelas
        nilai = kkm.raport_set.all()
        rekap_list = get_rekap(kkm, nilai)
        context['tahun'] = tahun
        context['kelas'] = kelas
        context['mypk'] = self.kwargs['pk']
        context['guru'] = guru
        context['nama_mapel'] = nama_mapel
        context['nilai'] = rekap_list
        return context

class RaportPrintView(LoginRequiredMixin,View):
    model = Raport
    template_name = 'raport/raport_print.html'

    def get(self,request, pk):
        kkm = KkmMapel.objects.get(pk=pk)
        guru = kkm.mapel.guru.nama
        nama_mapel = kkm.mapel.mapel.nama_mapel
        tahun = kkm.tahun.tahun
        kelas = kkm.kelas.nama_kelas
        nilai = kkm.raport_set.all()
        rekap_list = get_rekap(kkm, nilai)
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

class RaportView(LoginRequiredMixin,ListView):
    model = Raport
    template_name = 'raport/index.html'

def get_guru(userid):
    return Guru.objects.get(user=userid)

def get_kkm(id):
    return KkmMapel.objects.filter(mapel_id=id)

def get_mengajar(guru):
    return Mengajar.objects.filter(guru_id=guru.id)

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

def get_rekap(kkm, nilai):
    rekap_list = []
    for ni in nilai:
        rekap = {}
        rekap['nis'] = ni.siswa.nis
        rekap['siswa'] = ni.siswa.nama
        rekap['angka_pengetahuan'] = ni.pengetahuan
        rekap['angka_keterampilan'] = ni.keterampilan
        rekap['predikat_pengetahuan'] = get_predikat(kkm.pengetahuan, ni.pengetahuan)
        rekap['predikat_keterampilan'] = get_predikat(kkm.ketrampilan, ni.keterampilan)
        rekap['desc_pengetahuan'] = kkm.descmapel_set.get(
            predikat=get_predikat(kkm.pengetahuan, ni.pengetahuan)).pengetahuan
        rekap['desc_keterampilan'] = kkm.descmapel_set.get(
            predikat=get_predikat(kkm.ketrampilan, ni.keterampilan)).ketrampilan
        rekap_list.append(rekap)
    return rekap_list