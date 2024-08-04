from django.contrib import admin
from base.models import Tag,Category,Item
from django.contrib.auth.models import Group

class TagInline(admin.TabularInline):
    model = Item.tags.through
 
 
class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Item,ItemAdmin)
admin.site.unregister(Group)