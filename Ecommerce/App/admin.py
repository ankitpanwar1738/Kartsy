from django.contrib import admin
from.models import *
# Register your models here.

class Product_imgs(admin.TabularInline):
    model=Product_Image

class Additional_info(admin.TabularInline):
    model=Additional_Information


class Product_Admin(admin.ModelAdmin):
    inlines=(Product_imgs,Additional_info)
    list_display=('product_name','Categories','color','section')
    list_editable=('Categories','section','color')



class OrderItemTubleinline(admin.TabularInline):
    model=OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemTubleinline]



admin.site.register(slider)
admin.site.register(banner_area)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product,Product_Admin)
admin.site.register(Section)
admin.site.register(Additional_Information)
admin.site.register(Product_Image)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Coupon_Code)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(banner)
admin.site.register(banner_Section)
admin.site.register(ban_section)






