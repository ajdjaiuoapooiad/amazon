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
    
class CategoryListView(generic.ListView):
    model=Item
    template_name='pages/list.html'
    paginate_by=2
    
    def get_queryset(self):
        self.category=Category.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(category=self.category)
    def get_context_data(self,**kwargs):         #文字列を指定
        context=super().get_context_data(**kwargs)
        context['title']=f'Category #{self.category.name}'
        return context
    
class TagListView(generic.ListView):
    model=Item
    template_name='pages/list.html'
    paginate_by=2
    
    def get_queryset(self):
        self.category=Category.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(category=self.category)
    def get_context_data(self,**kwargs):         #文字列を指定
        context=super().get_context_data(**kwargs)
        context['title']=f'Category #{self.category.name}'
        return context