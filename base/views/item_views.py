from django.shortcuts import render
from django.views import generic
from base.models import Item,Category,Tag


class ListView(generic.ListView):
    model=Item
    template_name='pages/index.html'
    queryset=Item.objects.filter(is_published=True)
    
class ItemDetailView(generic.DetailView):
    model=Item
    template_name='pages/item.html'
    