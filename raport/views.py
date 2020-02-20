import io
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View
from django.forms.models import inlineformset_factory

from guru.models import Guru
from mapel.models import KkmMapel,Kelas,Mapel,DescMapel,Mengajar
from siswa.models import Kelas as KelasSiswa,Siswa
from walikelas.models import WaliKelas
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
        wali = WaliKelas.objects.get(guru_id=guru.id)
        nilai = KelasSiswa.objects.filter(Q(kelas_id=wali.kelas) & Q(tahun_id=wali.tahun))

        context = {
            'jadwal': jadwal,
            'title': 'Nilai siswa',
            'wali': wali,
            'nilai': nilai
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

class RaportSiswaView(LoginRequiredMixin,ListView):
    model = Raport
    template_name = 'raport/raport_siswa.html'
    def get_context_data(self, **kwargs):
        context = super(RaportSiswaView, self).get_context_data(**kwargs)
        idsiswa = self.kwargs['siswa']
        idkelas = self.kwargs['kelas']
        idtahun = self.kwargs['tahun']
        siswa = KelasSiswa.objects.get(Q(siswa_id=idsiswa) & Q(tahun_id=idtahun) & Q(kelas_id=idkelas))
        raport = Raport.objects.filter(Q(siswa_id=idsiswa) & Q(mapel__tahun_id=idtahun) & Q(mapel__kelas_id=idkelas))
        rekap_list = raport_list(raport)
        context['raport'] = rekap_list
        context['siswa'] = siswa.siswa.nama
        context['nis'] = siswa.siswa.nis
        context['kelas'] = siswa.kelas.nama_kelas
        context['tahun'] = siswa.tahun
        return context

class RaportSiswaDownload(LoginRequiredMixin,View):
    def get(self,request, siswa,kelas,tahun):
        datasiswa = KelasSiswa.objects.get(Q(siswa_id=siswa) & Q(tahun_id=tahun) & Q(kelas_id=kelas))
        raport = Raport.objects.filter(Q(siswa_id=siswa) & Q(mapel__tahun_id=tahun) & Q(mapel__kelas_id=kelas))
        rekap_list = raport_list(raport)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
        cell_format.set_text_wrap()
        worksheet.set_column('B:B', 25)
        worksheet.set_column('F:F', 25)
        worksheet.set_column('J:J', 25)
        worksheet.write('A1', 'Nama Sekolah')
        worksheet.write('A2','Alamat')
        worksheet.write('A3','Nama Siswa')
        worksheet.write('A4','Nomor Induk/ NISN')
        worksheet.write('C1', "SMK Ma'arif Nurul ")
        worksheet.write('C2', 'Taruban Kulon, Tuksono, Sentolo, Kulon Progo, Yogyakarta 55664')
        worksheet.write('C3', datasiswa.siswa.nama)
        worksheet.write('C4', datasiswa.siswa.nis)
        worksheet.write('H1', 'Kelas')
        worksheet.write('H2', 'SMT')
        worksheet.write('H3', 'Tahun')
        worksheet.write('J1', datasiswa.kelas.nama_kelas)
        worksheet.write('J2', 'SMT')
        worksheet.write('J3', datasiswa.tahun.tahun)

        worksheet.merge_range('A15:A16','NO',cell_format)
        worksheet.merge_range('B15:B16', 'Mata Pelajaran', cell_format)
        worksheet.merge_range('C15:F15', 'Pengetahuan', cell_format)
        worksheet.merge_range('G15:J15', 'Keterampilan', cell_format)
        worksheet.merge_range('A17:J17', 'Keterampilan', cell_format)
        worksheet.write('C16', 'KKM', cell_format)
        worksheet.write('D16', 'Angka', cell_format)
        worksheet.write('E16', 'Predikat', cell_format)
        worksheet.write('F16', 'Deskripsi', cell_format)
        worksheet.write('G16', 'KKM', cell_format)
        worksheet.write('H16', 'Angka', cell_format)
        worksheet.write('I16', 'Predikat', cell_format)
        worksheet.write('J16', 'Deskripsi', cell_format)
        worksheet.write('A17', 'Muatan Nasional', cell_format)
        row = 18
        num = 1
        for nilai in rekap_list:
            worksheet.write(row, 0, num, cell_format)
            worksheet.write(row, 1, nilai['mapel'], cell_format)
            worksheet.write(row, 2, nilai['kkm_pengetahuan'], cell_format)
            worksheet.write(row, 3, nilai['angka_pengetahuan'], cell_format)
            worksheet.write(row, 4, nilai['predikat_pengetahuan'], cell_format)
            worksheet.write(row, 5, nilai['desc_pengetahuan'], cell_format)
            worksheet.write(row, 6, nilai['kkm_keterampilan'], cell_format)
            worksheet.write(row, 7, nilai['angka_keterampilan'], cell_format)
            worksheet.write(row, 8, nilai['predikat_keterampilan'], cell_format)
            worksheet.write(row, 9, nilai['desc_keterampilan'], cell_format)
            row += 1
            num += 1

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'nilai_raport.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

class RaportSiswaPrint(LoginRequiredMixin,View):
    #template_name = 'raport/raport_siswa_print.html'
    def get(self,request,siswa,kelas,tahun):
        datasiswa = KelasSiswa.objects.get(Q(siswa_id=siswa) & Q(tahun_id=tahun) & Q(kelas_id=kelas))
        raport = Raport.objects.filter(Q(siswa_id=siswa) & Q(mapel__tahun_id=tahun) & Q(mapel__kelas_id=kelas))
        rekap_list = raport_list(raport)
        parrams = {
            'tahun': datasiswa.tahun.tahun,
            'kelas': datasiswa.kelas.nama_kelas,
            'siswa': datasiswa.siswa.nama,
            'nis': datasiswa.siswa.nis,
            'raport': rekap_list,
            'request': request
        }
        return Render.render('raport/raport_siswa_print.html', parrams)

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

def raport_list(raport):
    rekap_list = []
    for nilai in raport:
        rekap = {}
        rekap['nis'] = nilai.siswa.nis
        rekap['siswa'] = nilai.siswa.nama
        rekap['mapel'] = nilai.mapel.mapel.mapel.nama_mapel
        rekap['kkm_pengetahuan'] = nilai.mapel.pengetahuan
        rekap['angka_pengetahuan'] = nilai.pengetahuan
        rekap['predikat_pengetahuan'] = get_predikat(nilai.mapel.pengetahuan, nilai.pengetahuan)
        rekap['desc_pengetahuan'] = nilai.mapel.descmapel_set.get(
            predikat=get_predikat(nilai.mapel.pengetahuan, nilai.pengetahuan)).pengetahuan
        rekap['kkm_keterampilan'] = nilai.mapel.ketrampilan
        rekap['angka_keterampilan'] = nilai.keterampilan
        rekap['predikat_keterampilan'] = get_predikat(nilai.mapel.ketrampilan, nilai.keterampilan)
        rekap['desc_keterampilan'] = nilai.mapel.descmapel_set.get(
            predikat=get_predikat(nilai.mapel.ketrampilan, nilai.keterampilan)).ketrampilan
        rekap_list.append(rekap)
    return rekap_list