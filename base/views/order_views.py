from django.views import generic
from base.models import Order
import json


class OrderListView(generic.ListView):
    model=Order
    template_name='pages/order_list.html'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    
class OrderDetailView(generic.DetailView):
    model=Order
    template_name='pages/order_detail.html'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        obj=self.get_object()
        
        context['items']=json.loads(obj.items)
        context['shipping']=json.loads(obj.shipping)
        return context