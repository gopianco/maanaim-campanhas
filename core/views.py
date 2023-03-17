from django.views.generic import TemplateView

from .models import Bread, SaleItem

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['product_list'] = Bread.objects.all()
        return context
    
    def add_to_bag():
        item = SaleItem()
        return item
