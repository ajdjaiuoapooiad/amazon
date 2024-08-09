from django.shortcuts import render,redirect
from django.conf import settings
from django.views import generic
from base.models import Item
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class CartListView(LoginRequiredMixin,generic.ListView):
    model=Item
    template_name='pages/cart_list.html'
    
    def get_queryset(self):
        cart=self.request.session.get('cart',None)
        if cart is None or len(cart)==0:
            return redirect('/')
        self.queryset= []
        self.totall=0
        for item_pk,quantity in cart['items'].items():
            obj=Item.objects.get(pk=item_pk)
            obj.quantity=quantity
            obj.subtotall=int(obj.price*quantity)
            self.queryset.append(obj)
            self.totall += obj.subtotall
        self.tax_included_totall=int(self.totall*(settings.TAX_RATE+1))
        cart['totall']=self.totall
        cart['tax_included_totall']=self.tax_included_totall
        self.request.session['cart']=cart
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["totall"] = self.totall
            context["tax_included_totall"] = self.tax_included_totall
        except Exception:
            pass
        return context
 
   
class AddCartView(LoginRequiredMixin,generic.View):
    
    def post(self,request):
        item_pk=request.POST.get('item_pk') #item.name
        quantity=int(request.POST.get('quantity')) #item.amount
        cart=request.session.get('cart',None)
        messages.info(self.request,'カートに追加しました。') #
        if cart is None or len(cart)==0:
            items=OrderedDict()
            cart={'items':items}
        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        else:
            cart['items'][item_pk] = quantity
        request.session['cart']=cart
        return redirect('/cart/')
    
@login_required   
def remove_from_cart(request,pk):
    cart=request.session.get('cart',None)
    if cart is not None:
        del cart['items'][pk]
        request.session['cart']=cart
    return redirect('/cart/')
    
    

    