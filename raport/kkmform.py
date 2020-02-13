from django.forms.models import inlineformset_factory
from .models import KkmMapel,DescMapel

KkmFormset = inlineformset_factory(KkmMapel,DescMapel,fields=['mapel','pengetahuan','ketrampilan','predikat'],exclude=[],can_delete=False)