from django.shortcuts import render,redirect
from App.models import slider,banner_area,Main_Category,Product,Category,Color,Brand,Coupon_Code,Order,OrderItem,Sub_Category,Wishlist,banner, ban_section,banner_Section,ProductRating
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.db.models import Min, Max,Sum
from cart.cart import Cart
from django.shortcuts import render, redirect, get_object_or_404
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from App.models import Product



client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))



# Create your views here.

def Base(request):
    products = Product.objects.all()
    context={
        'products':products,
    }

    return render(request,'base.html',context)


def Home(request):

    products = Product.objects.all()

    for product in products:
        ratings = product.ratings.all()
        if ratings.exists():
            avg = sum(r.rating for r in ratings) / ratings.count()
            product.avg_rating = round(avg, 1)
        else:
            product.avg_rating = 0
        product.full_stars = int(product.avg_rating)
        product.empty_stars = 5 - product.full_stars

    Sliders = slider.objects.all().order_by('-id')[0:4]
    Banner = banner_area.objects.all().order_by('-id')[0:3]
    main_cate = Main_Category.objects.all().order_by('-id')
    products = Product.objects.filter(section__name='Top Deals Of The Day')
    featured_products = Product.objects.filter(section__name='Top Featured Products').order_by('-id')[:4]
    ban = banner.objects.all().order_by('-id')
    recommended_products = Product.objects.filter()
    brands = Brand.objects.all()
    bann = ban_section.objects.filter(sectionn__name='Hot Deals')
    banne = ban_section.objects.filter(sectionn__name='Electronic Deals')
    bannee = ban_section.objects.filter(sectionn__name='Hot Products')

    context = {
        'Sliders': Sliders,
        'Banner': Banner,
        'main_cate': main_cate,
        'products': products,
        'featured_products': featured_products, 
        'ban': ban,
        'recommended_products': recommended_products,
        'brands': brands,
        'bann': bann,
        'banne': banne,
        'bannee': bannee,
    }

    return render(request, 'Main/home.html', context)



def ABOUT(request):
     return render(request,'Main/about.html')


def CONTACT(request):
     return render(request,'Main/contactus.html')


def PRODUCT(request):
    # Get filter parameters from request
    category_ids = request.GET.getlist('category')
    brand_ids = request.GET.getlist('brand')
    color_id = request.GET.get('colorID')
    min_price_val = request.GET.get('min_price')
    max_price_val = request.GET.get('max_price')

    # Convert price strings to floats safely
    try:
        min_price_val = float(min_price_val) if min_price_val else None
        max_price_val = float(max_price_val) if max_price_val else None
    except ValueError:
        min_price_val = None
        max_price_val = None

    # Start with all products
    products = Product.objects.all()

    # Apply filters independently
    if category_ids:
        products = products.filter(Categories__id__in=category_ids)

    if brand_ids:
        products = products.filter(Brand__id__in=brand_ids)

    if color_id:
        products = products.filter(color__id=color_id)

    if min_price_val is not None and max_price_val is not None:
        products = products.filter(price__gte=min_price_val, price__lte=max_price_val)
    elif min_price_val is not None:
        products = products.filter(price__gte=min_price_val)
    elif max_price_val is not None:
        products = products.filter(price__lte=max_price_val)

    # Get global price range for slider
    price_range = Product.objects.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )

    # Get data for filters
    categories = Category.objects.annotate(product_count=Count('product'))
    colors = Color.objects.all()
    brands = Brand.objects.all()



    paginator = Paginator(products, 20)  # 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': categories,
        'color': colors,
        'brand': brands,
        'product': products,
        'selected_category': list(map(int, category_ids)) if category_ids else [],
        'selected_color': int(color_id) if color_id else None,
        'selected_brand': list(map(int, brand_ids)) if brand_ids else [],
        'min_price': price_range['min_price'],
        'max_price': price_range['max_price'],
        'product': page_obj,
        'request': request,  
    }

    return render(request, 'product/product.html', context)




def PRODUCT_DETAILS(request,slug):
    product=Product.objects.filter(slug = slug)
    if product.exists ():
            product=Product.objects.get(slug = slug)
    else:
         return redirect('404')

    context={
        'product':product,
    }
    return render(request,'product/product_detail.html',context)


def Error404(request):
    return render(request,'error/404.html')

def MY_ACCOUNT(request):
     return render(request,'account/my-account.html')

def REGISTER(request):
     if request.method=='POST':
          username=request.POST.get('username')
          email=request.POST.get('email')
          password=request.POST.get('password')

          if User.objects.filter(username=username).exists():
               messages.error(request,'username is already exists')
               return redirect('login')
          
          if User.objects.filter(email=email).exists():
               messages.error(request,'email is already exists')
               return redirect('login')

          user=User(
               username=username,
               email=email,
               password=password,
               )
          user.set_password(password)
          user.save()
          return redirect('login')
     

def LOGIN(request):
     if request.method == 'POST':
          username=request.POST.get('username')
          password=request.POST.get('password')

          user=authenticate(request,username=username,password=password)
          if user is not None:
               login(request,user)
               return redirect('home')
          else:
               messages.error(request,'Email And Password are Invalid')
               return redirect('login')
     # return render (request,'account/my-account.html')


@login_required(login_url='/accounts/login/')
def PROFILE(request):
     return render (request,'profile/profile.html')


@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = request.user  #  get the current logged-in user

        # Update user fields
        user.username = username
        user.first_name = fname
        user.last_name = lname
        user.email = email

        if password:  # Only update if password is not empty
            user.set_password(password)

        user.save()

        # Re-authenticate the user if password changed
        if password:
            login(request, user)

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return redirect('profile')




@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    cart = request.session.get('cart', {})

    cart_total_amount = 0
    for item in cart.values():
        if item:
            price = item.get('price', 0)
            quantity = item.get('quantity', 1)
            cart_total_amount += price * quantity

    packing_cost = sum(item.get('packing_cost', 0) for item in cart.values() if item)
    tax = sum(item.get('tax', 0) for item in cart.values() if item)

    coupon = None
    valid_coupon = None
    invalid_coupon = None 
    coupon_discount = 0  

    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_Code.objects.get(code=coupon_code)
                valid_coupon = 'Coupon is applicable on the current order!'
                coupon_discount = coupon.discount 
            except Coupon_Code.DoesNotExist:
                invalid_coupon = 'Invalid coupon code!'

    delivery_charge = 120 if cart_total_amount < 500 else 0

    discounted_amount = cart_total_amount
    if coupon_discount > 0:
        discounted_amount = cart_total_amount - (cart_total_amount * coupon_discount / 100)

    final_total = discounted_amount + packing_cost + tax + delivery_charge

    context = {
        'cart_total_amount': cart_total_amount,
        'packing_cost': packing_cost,
        'tax': tax,
        'delivery_charge': delivery_charge,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
        'coupon_discount': coupon_discount,
        'discounted_amount': discounted_amount,
        'final_total': final_total,
        'cart': cart,
    }

    return render(request, 'cart/cart_detail.html', context)





def Checkout(request):
    coupon_discount = None

    if request.method == "POST":
        coupon_discount = request.POST.get('coupon_discount')

    cart = request.session.get('cart', {})

    packing_cost = sum(i.get('packing_cost', 0) for i in cart.values() if i)
    tax = sum(i.get('tax', 0) for i in cart.values() if i)

    tax_and_packing_cost = packing_cost + tax

    context = {
        'tax_and_packing_cost': tax_and_packing_cost,
        'coupon_discount': coupon_discount,
    }

    try:
        payment = client.order.create(
            {
                'amount': 500,  
                'currency': 'INR',
                'payment_capture': '1'
            }
        )
        order_id = payment['id']

        context.update({
            'order_id': order_id,
            'payment': payment
        })

    except Exception as e:
        # Log the error or print it (for debugging)
        print(f"Razorpay API error: {e}")

        # Provide a fallback or friendly error message
        context.update({
            'error': "Payment service is temporarily unavailable. Please try again later."
        })

    return render(request, 'checkout/checkout.html', context)

import uuid
from django.db import IntegrityError

def generate_order_id():
    return str(uuid.uuid4())

def place_order(request):
    if request.method == 'POST':
        user = request.user
        cart = request.session.get('cart', {})

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        order_id = request.POST.get('order_id')

        # If no valid order_id is passed or it's a duplicate, generate a new one
        if not order_id or Order.objects.filter(order_id=order_id).exists():
            order_id = generate_order_id()

        try:
            order = Order.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                country=country,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                postcode=postcode,
                phone=phone,
                email=email,
                amount=amount,
                order_id=order_id
            )
        except IntegrityError:
            return render(request, 'cart/place_order.html', {
                'error': 'An error occurred while creating the order. Please try again.'
            })

        # TODO: Create Order Items here using the cart

        return render(request, 'cart/place_order.html', {
            'order_id': order.order_id,
            'success': True
        })

    return render(request, 'cart/place_order.html', {
        'message': 'Please place order via checkout form.'
    })


@csrf_exempt
def success(request):
    if request.method == 'POST':
        order_id = request.POST.get('razorpay_order_id')

        if order_id:
            try:
                order = Order.objects.get(payment_id=order_id)
                order.paid = True
                order.save()
                return render(request, 'cart/success.html', {'order': order})
            except Order.DoesNotExist:
                return render(request, 'cart/success.html', {'error': 'Order not found!'})
        else:
            return render(request, 'cart/success.html', {'error': 'Payment ID not provided.'})

    return redirect('home')  



def Department(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    products = Product.objects.filter(Categories=category)

    context = {
        'product': products,
        'selected_category': category
    }
    return render(request, 'product/department.html', context)




def SubCategoryView(request, sub_id):
    subcategory = get_object_or_404(Sub_Category, id=sub_id)
    
    products = Product.objects.filter(Categories=subcategory.category)

    context = {
        'product': products,
        'selected_subcategory': subcategory
    }
    return render(request, 'product/department.html', context)







def wishlist(request):
    if request.user.is_authenticated:
        items = Wishlist.objects.filter(user=request.user).select_related('product')
        return render(request, 'wishlist/wishlist.html', {'wishlist_items': items})
    else:
        return render(request, 'wishlist/wishlist.html', {'wishlist_items': []})




@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, 'Item added to wishlist!')
    else:
        messages.info(request, 'Item already in wishlist!')
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, 'Item removed from wishlist!')
    return redirect('wishlist')




def privacy(request):
    return render(request,'profile/privacy_policy.html')


def help_center(request):
    return render(request,'profile/help_center.html')


def search_results(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.filter(product_name__icontains=query)

    return render(request, 'profile/search_results.html', {
        'results': results,
        'query': query
    })




@login_required(login_url='/accounts/login/')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'orders': orders
    }
    return render(request, 'orders/my_orders.html', context)



def track_order(request, order_id):
 
    return render(request, 'track_order.html', {'order_id': order_id})



from django.views.decorators.http import require_POST


@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.cancelled:
        messages.warning(request, "This order is already cancelled.")
    elif order.delivered:
        messages.error(request, "Delivered orders cannot be cancelled.")
    else:
        order.cancelled = True
        order.save()
        messages.success(request, "Your order has been cancelled.")

    return redirect('myorders')  # Adjust this to your orders page name




@login_required
def submit_rating(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        review_text = request.POST.get('review', '')

        rating, created = ProductRating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating_value, 'review': review_text}
        )
        return redirect(product.get_absolute_url())
