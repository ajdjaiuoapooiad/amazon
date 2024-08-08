from django.contrib import admin
from base.models import Tag,Category,Item,User,Profile,Order
from django.contrib.auth.models import Group
from base.forms import UserCreateForm
from django.contrib.auth.admin import UserAdmin



class TagInline(admin.TabularInline):
    model = Item.tags.through
 
 
class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']
    
class ProfileInline(admin.StackedInline):
    model=Profile
    can_delete=False
    
class CustomAdomin(UserAdmin):
    fieldsets=(
        (None, {'fields':('username','email','password')}),
        (None,{'fields':('is_active','is_admin')}),
    )
    list_display=('username','email','is_active')
    list_filter=()
    ordering=()
    filter_horizontal=()
    
    add_fieldsets=(
        (None,{'fields':('username','email','is_active')}),
    )
    add_form=UserCreateForm
    inlines=(ProfileInline,)

# Register your models here.
admin.site.register(Order)
admin.site.register(User,CustomAdomin) #
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Item,ItemAdmin)
admin.site.unregister(Group)