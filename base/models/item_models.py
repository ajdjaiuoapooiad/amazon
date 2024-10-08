from django.db import models
import os
from django.utils.crypto import get_random_string

# urlから特定されないため
def create_id(): 
    return get_random_string(22)

def upload_image_to(instance, filename):
    item_id = str(instance.id)
    return os.path.join('static', 'items', item_id, filename)




class Category(models.Model):
    slug=models.CharField(max_length=32, primary_key=True)
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    slug=models.CharField(max_length=32, primary_key=True)
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name
    

class Item(models.Model):
    id=models.CharField(default=create_id, primary_key=True,
                          max_length=22, editable=False)
    name=models.CharField('商品名',max_length=100,)
    price=models.PositiveIntegerField('価格',default=0)
    stock=models.PositiveIntegerField('在庫',default=0)
    text=models.TextField('説明',blank=True)
    sold_count=models.PositiveIntegerField('売れ筋',default=0)
    is_published=models.BooleanField('公開',default=True)
    created_at=models.DateTimeField('作成日',auto_now_add=True)
    update_at=models.DateTimeField('更新日',auto_now=True)
    image = models.ImageField(
        default="", blank=True, upload_to=upload_image_to)

    
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    tags=models.ManyToManyField(Tag,blank=True)
    def __str__(self):
        return self.name
    