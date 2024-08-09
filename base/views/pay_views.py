from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from stripe.api_resources import tax_rate
from base.models import Item,Order
from django.views import generic
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
import json
from django.contrib import messages
 

stripe.api_key=settings.STRIPE_API_SECRET_KEY

class PaySuccessView(LoginRequiredMixin,generic.TemplateView):
    template_name='pages/success.html'
    
    def get(self,request,*args,**kwargs):
        
         # カート情報削除
        messages.success(self.request,'支払いが完了しました。') #
        del request.session['cart']
        return super().get(request,*args,**kwargs)
        
        
class PayCancelView(LoginRequiredMixin,generic.TemplateView):
    template_name='pages/cancel.html'
    
    def get(self,request,*args,**kwargs):
        # 最新のOrderオブジェクトを取得　　追記
        order=Order.objects.filter(
            user=request.user).order_by('-created_at')[0] #一番最新の注文を取得
    
        # 在庫数と販売数を元の状態に戻す
        for elem in json.loads(order.items):   #elemとは？
            item=Item.objects.get(pk=elem['pk'])
            item.sold_count-=elem['quantity']
            item.stock+=elem['quantity']
            item.save()
        # is_confirmedがFalseであれば削除（仮オーダー削除）
        if not order.is_confirmed:
            order.delete()
        messages.error(self.request,'支払いがキャンセルされました。') #
        return super().get(request,*args,**kwargs)
        
tax_rate=stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE*100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)
    
    
def create_line_item(unit_amount,name,quantity):
    return {
        'price_data':{
            'currency':'JPY',
            'unit_amount':unit_amount,
            'product_data':{'name':name}
        },
        'quantity':quantity,
        'tax_rates':[tax_rate.id],
        
    }
    
#プロフィールが埋まっているかの確認
def check_profile_filled(profile):
    if profile.name is None or profile.name == '':
        return False
    
    elif profile.prefecture is None or profile.prefecture == '':
        return False
    elif profile.city is None or profile.city == '':
        return False
    elif profile.address1 is None or profile.address1 == '':
        return False
    return True
    
class PayWithStripe(LoginRequiredMixin,generic.View):
    
    def post(self,request,*args,**kwargs):
        
        # プロフィールが埋まっているかどうか確認
        if not check_profile_filled(request.user.profile):
            messages.error(request, 'プロフィールを埋めてください。')
            return redirect('/profile/')
 
        #カートが空の場合
        cart=request.session.get('cart',None)
        if cart is None or len(cart)==0:
            messages.error(self.request,'カートが空です。') #
            return redirect('/')
        
      
        items=[]                #空のitem 追記
        line_items=[]
        for item_pk,quantity in cart['items'].items():
            item=Item.objects.get(pk=item_pk)
            line_item=create_line_item(
                item.price, item.name, quantity)
            line_items.append(line_item)
            
            # Orderモデル用に追記 for文の中に 辞書として
            items.append({
                'pk':item_pk,
                'name':item.name,
                'image':str(item.image),
                'price':item.price,
                'quantity':quantity,
            })
            # 在庫をこの時点で引いておく、注文キャンセルの場合は在庫を戻す
            # 販売数も加算しておく
            
            item.stock -= quantity
            item.sold_count += quantity
            item.save()
            
        # 仮注文を作成（is_confirmed=Flase) forの外に
        Order.objects.create(
            user=request.user,
            uid=request.user.pk,
            shipping=serializers.serialize('json',[request.user.profile]),  #
            items=json.dumps(items),                            #よくわからない
            amount=cart['totall'],
            tax_included=cart['tax_included_totall'],
            
        )
            
            
            
                        
        checkout_session =stripe.checkout.Session.create(
            #customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.MY_URL}/pay/success/',
            cancel_url=f'{settings.MY_URL}/pay/cancel/',
        )
        return redirect(checkout_session.url)

