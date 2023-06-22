from django.db import models
from django.utils.text import slugify 
from django.utils.crypto import get_random_string 
from datetime import datetime

class Bread(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=5, decimal_places=2)
    slug = models.SlugField('Identificador', unique=True, editable=False)
    image = models.ImageField('Imagem', upload_to='bread', blank=True, null=True)
    weight = models.DecimalField('Peso em Kg', max_digits=5, decimal_places=3)

    class Meta:
        verbose_name = 'Pão'
        verbose_name_plural = 'Pães'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Bread, self).save(*args, **kwargs)


class SaleItem(models.Model):
    item =  models.OneToOneField(Bread, on_delete=models.CASCADE, verbose_name='Item', blank=False, null=False)
    quantity = models.PositiveSmallIntegerField('Quatidade')
    price_sum = models.DecimalField('Sub Total', max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Item de venda'
        verbose_name_plural = 'Itens'

    def __str__(self):
        return self.item.name
    
    def get_price_sum(self):
        return self.quatity * self.item.price
    
    def save(self, *args, **kwargs):
        self.price_sum = self.get_price_sum()
        super(SaleItem, self).save(*args, **kwargs)


class Sale(models.Model):
    items = models.ForeignKey(SaleItem, on_delete=models.CASCADE, verbose_name='items', blank=False, null=False)
    total_price = models.DecimalField('Preço Total', max_digits=6, decimal_places=2)
    customer_name = models.CharField('Nome do Cliente', max_length=100)
    customer_phone_number = models.CharField('Telefone do Cliente', max_length=11)
    code = get_random_string(5)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        return self.code
    
    def get_sum_of_items(self):
        return sum(self.items.priceSum)
    
    def save(self, *args, **kwargs):
        self.total_price = self.get_sum_of_items()
        super(SaleItem, self).save(*args, **kwargs)


class Campaing(models.Model):
    delivery_date = models.DateTimeField('Data de Entrega', auto_now=False, auto_now_add=False, blank=True, null=True)
    slug = models.SlugField('Identificador', unique=True, editable=True)
    sales = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Vendas', blank=True, null=True)
    active = models.BooleanField('Ativa', default=True)
    endDate = models.DateTimeField('Data de Entrega', auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Campanha'
        verbose_name_plural = 'Campanhas'

    def __str__(self):
        return str(self.delivery_date)
    
    def save(self, *args, **kwargs):
        if not self.active:
            self.endDate = datetime.now()
        super(Campaing, self).save(*args, **kwargs)


class InstagramUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField('Nome de Usuario', max_length=100, unique=True)
    post_date = models.DateTimeField('Data do post', auto_now_add=True, blank=False)
    post_id = models.CharField('Id do post', max_length=100)
    rewarded = models.BooleanField('Recompensado', default=False, blank=True)
    rewarded_date = models.DateTimeField('Data da recompensa', auto_now_add=False, blank=True, null=True)
    token = models.CharField("Token de verificacao", max_length=6, null=True )
    json = models.JSONField(default='', blank=True)


