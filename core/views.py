from django.views.generic import TemplateView

from .models import Bread, SaleItem, Campaing

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        product_list = Bread.objects.all()

        sale_item_list = list()
        for product in product_list:
            sale_item_list.append(SaleItem(item = product, quantity = 1, price_sum = product.price)) 
        
        campaing = Campaing.objects.filter(active=True).first()

        context['item_sale_list'] = sale_item_list
        context['campaing_date'] = campaing.delivery_date

        return context
    
class SaleItemUpdateView():
    model = SaleItem
