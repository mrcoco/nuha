from django.forms.models import inlineformset_factory
from mapel.models import KkmMapel,DescMapel

KkmFormset = inlineformset_factory(KkmMapel,DescMapel,fields=['mapel','pengetahuan','ketrampilan','predikat'],exclude=[],can_delete=False,max_num=4,min_num=4)