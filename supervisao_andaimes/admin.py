from django.contrib import admin
from .models import Empresa, Inspecao, ItemInspecao, ImagemInspecao
from django.utils.html import format_html
from django.urls import reverse

class ItemInspecaoInline(admin.TabularInline):
    model = ItemInspecao
    extra = 0
    fields = ('categoria', 'item', 'status', 'desvio_identificado', 'acao_corretiva')
    show_change_link = True

class ImagemInspecaoInline(admin.TabularInline):
    model = ImagemInspecao
    extra = 0
    fields = ('imagem', 'legenda')
    show_change_link = True

@admin.register(Inspecao)
class InspecaoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'empresa', 'inspetor', 'data_inspecao', 'status_final', 'gerar_pdf_link')
    search_fields = ('codigo', 'empresa__nome', 'inspetor')
    list_filter = ('status_final', 'data_inspecao')
    inlines = [ItemInspecaoInline, ImagemInspecaoInline]

    def gerar_pdf_link(self, obj):
        url = reverse('gerar_pdf_inspecao', args=[obj.pk])
        return format_html(f'<a class="button" href="{url}" target="_blank">📄 PDF</a>')

    gerar_pdf_link.short_description = "Relatório"

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj')
    search_fields = ('nome', 'cnpj')
