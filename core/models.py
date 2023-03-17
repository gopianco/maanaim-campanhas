from django.db import models
from django.utils.text import slugify 

class Bread(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=5, decimal_places=2)
    slug = models.SlugField('Identificador', unique=True, editable=False)
    image = models.ImageField('Imagem', upload_to='bread', blank=True, null=True)
    weight = models.PositiveIntegerField('Peso em Kg')

    class Meta:
        verbose_name = 'Pão'
        verbose_name_plural = 'Pães'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.type_frame)
        super(Bread, self).save(*args, **kwargs)