from django.db import models

# Opções de status dos itens de inspeção
STATUS_OPCOES = [
    ('C', 'Conforme'),
    ('NC', 'Não Conforme'),
    ('NI', 'Não Inspecionado'),
]

# Seções fixas da inspeção
CATEGORIA_CHOICES = [
    ('plataforma', 'Plataforma'),
    ('guincho', 'Guincho'),
    ('contrapesos', 'Contrapesos'),
    ('ancoragem', 'Ancoragem'),
    ('linha_vida', 'Linha de Vida'),
]

# Status final da inspeção
STATUS_FINAL_CHOICES = [
    ('liberado', 'Liberado'),
    ('nao_liberado', 'Não Liberado'),
    ('desativado', 'Desativado'),
]


class TopicoPadrao(models.Model):
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    ordem = models.CharField(max_length=10, help_text="Ex: 1.1, 2.1, etc.")
    descricao = models.CharField(max_length=255)

    class Meta:
        ordering = ['categoria', 'ordem']

    def __str__(self):
        return f"{self.ordem} - {self.get_categoria_display()} - {self.descricao}"


class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, blank=True, null=True)

    def __str__(self):
        return self.nome


class Inspecao(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    inspetor = models.CharField(max_length=255)
    tecnico_seguranca = models.CharField(max_length=255)
    encarregado = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50, unique=True)
    data_inspecao = models.DateField()
    andaime = models.CharField(max_length=100)
    status_final = models.CharField(
        max_length=20,
        choices=STATUS_FINAL_CHOICES,
        default='nao_liberado'
    )

    def __str__(self):
        return f"{self.codigo} - {self.empresa.nome}"


class ItemInspecao(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.CASCADE, related_name="itens")
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    ordem = models.CharField(max_length=10, help_text="Ex: 1.1, 2.1, etc.")
    item = models.CharField(max_length=255)
    status = models.CharField(max_length=2, choices=STATUS_OPCOES)
    desvio_identificado = models.TextField(blank=True, null=True)
    acao_corretiva = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ordem} - {self.get_categoria_display()} - {self.item} ({self.get_status_display()})"

    class Meta:
        ordering = ['categoria', 'ordem']


class ImagemInspecao(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to='inspecoes/')
    legenda = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Imagem {self.id} - {self.inspecao.codigo}"

