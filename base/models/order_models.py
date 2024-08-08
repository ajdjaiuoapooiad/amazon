from django.db import models
import datetime
from django.contrib.auth import get_user_model  #モデルを引っ張ってくる

def custom_timestamp_id():
    dt=datetime.datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f') #idに文字列を使う　固定


class Order(models.Model):
    id=models.CharField(default=custom_timestamp_id,max_length=50,editable=False,primary_key=True)
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    uid=models.CharField(max_length=50,editable=False)
    is_confirmed=models.BooleanField(default=False)  #多分２択
    amount=models.PositiveIntegerField(default=0)
    tax_include=models.PositiveIntegerField(default=0)
    items=models.JSONField()
    shipping=models.JSONField()
    shipped_at=models.DateTimeField(blank=True,null=True)
    cansel_at=models.DateTimeField(blank=True,null=True)
    memo=models.TextField(blank=True)
    created_at=models.DateTimeField('日付',auto_now_add=True)
    updated_at=models.DateTimeField('更新日',auto_now=True)
    
    def __str__(self):
        return self.id