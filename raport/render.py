from io import BytesIO
from  django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

class Render:
    def render(path: str, parrams: dict):
        template = get_template(path)
        html = template.render(parrams)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)