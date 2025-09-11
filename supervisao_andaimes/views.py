import os
from collections import defaultdict
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from .models import Inspecao

def link_callback(uri, rel):
    """
    Converte caminhos de mídia e estáticos para caminhos absolutos do sistema de arquivos.
    Necessário para que o xhtml2pdf encontre as imagens.
    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(f"Arquivo não encontrado: {path}")
    return path

def gerar_pdf_inspecao(request, pk):
    inspecao = get_object_or_404(Inspecao, pk=pk)

    # Agrupando os itens da inspeção por categoria
    itens_por_categoria = defaultdict(list)
    for item in inspecao.itens.all().order_by('categoria', 'ordem'):
        itens_por_categoria[item.get_categoria_display()].append(item)

    template_path = 'pdf_inspecao.html'
    context = {
        'inspecao': inspecao,
        'itens_por_categoria': dict(itens_por_categoria),
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="inspecao_{inspecao.codigo}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response
