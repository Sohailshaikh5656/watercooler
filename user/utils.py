import hashlib
from datetime import datetime

def supplier_token_generator(supplier):
    salt = hashlib.sha256(str(supplier.pk).encode()).hexdigest()[:5]
    hash = hashlib.sha256(str(supplier.pk).encode() + str(salt).encode() + str(datetime.now()).encode()).hexdigest()
    return hash


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
