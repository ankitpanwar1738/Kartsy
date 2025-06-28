from django.contrib import admin
from django.urls import path,include
from.import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import add_to_wishlist, wishlist, remove_from_wishlist

urlpatterns = [
    path('404',views.Error404,name='404'),
    path('base', views.Base,name='base'),
    path('',views.Home,name='home'),
    path('about',views.ABOUT,name='about'),
    path('contact',views.CONTACT,name='contact'),
    path('products/',views.PRODUCT,name='product'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('product/<slug:slug>/',views.PRODUCT_DETAILS,name='product_detail'),
    path('account/my-account',views.MY_ACCOUNT,name='my_account'),
    path('account/register',views.REGISTER,name='handleregister'),
    path('account/login',views.LOGIN,name='handlelogin'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('account/profile',views.PROFILE,name='profile'),
    path('account/profile/update',views.PROFILE_UPDATE,name='profile_update'),

    
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('checkout/',views.Checkout,name='checkout'),
    path('place_order/',views.place_order,name='place_order'),
    path('success',views.success,name='success'),
    path('department/<int:category_id>/', views.Department, name='department'),
    path('subcategory/<int:sub_id>/', views.SubCategoryView, name='subcategory'),
   

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('privacy-policy',views.privacy,name='privacy'),
    path('help-center',views.help_center,name='help_center'),
    path('search/', views.search_results, name='search_results'),
    path('my-orders/', views.my_orders, name='myorders'),
    path('track-order/<str:order_id>/', views.track_order, name='track_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('rate/<slug:slug>/', views.submit_rating, name='submit_rating'),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)