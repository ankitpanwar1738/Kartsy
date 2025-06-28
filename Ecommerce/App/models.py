from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.
class slider(models.Model):

    DISCOUNT_DEAL=(
        ('Hot DEALS','HOT DEALS'),
        ('New Arraivels','New Arraivels')
    )

    Image=models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal=models.CharField(choices=DISCOUNT_DEAL,max_length=100)
    Brand_Name=models.CharField(max_length=200)
    Discount=models.IntegerField()
    Link=models.CharField(max_length=200)
    SALE=models.IntegerField()

    def __str__(self):
        return self.Brand_Name
    

class banner_area(models.Model):
    Image=models.ImageField(upload_to='media/banner_img')
    Discount_Deal=models.CharField( max_length=100)
    Quote=models.CharField(max_length=100)
    Discount=models.IntegerField()
    link_url = models.URLField(blank=True, null=True, help_text="Enter internal or external URL to redirect when clicked")

    def __str__(self):
        return self.Quote
    



class Main_Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    main_category=models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name + '--' + self.main_category.name
    

class Sub_Category(models.Model):
        category=models.ForeignKey(Category,on_delete=models.CASCADE)
        name=models.CharField(max_length=100)


        def __str__(self):
           return self.category.main_category.name + "--" +self.category.name + '--' + self.name
        
class Section(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Color(models.Model):
    code=models.CharField(max_length=100)

    def __str__(self):
        return self.code
    
class Brand(models.Model):
    name=models.CharField(max_length=200)
    image = models.ImageField(upload_to='brands/',null=True)


    def __str__(self):
        return self.name
    

class Coupon_Code(models.Model):
    code=models.CharField(max_length=100)
    discount=models.IntegerField()



class Product(models.Model):
    is_recommended = models.BooleanField(default=False)



class Product(models.Model):
    product_name = models.CharField(max_length=255) 
    total_quantity=models.IntegerField()
    Availability=models.IntegerField()
    featured_image=models.ImageField(upload_to='fimg')
    product_name=models.CharField(max_length=100)
    Brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    price=models.IntegerField()
    Discount=models.IntegerField(null=True,blank=True)
    tax=models.IntegerField(null=True)
    packing_cost=models.IntegerField(null=True)
    Product_Information=RichTextField(null=True)
    color=models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
    model_name=models.CharField(max_length=200)
    Categories=models.ForeignKey(Category,on_delete=models.CASCADE)
    Tags=models.CharField(max_length=100)
    Description=RichTextField()
    section=models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    slug=models.SlugField(default='',max_length=500,null=True,blank=True)
    
    rating = models.FloatField(default=0)  # Value between 0 and 5
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name
    

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    class Meta:
        db_table='App_Product'


def create_slug(instance,new_slug=None):
    slug=slugify(instance.product_name)
    if new_slug is not None:
        slug=new_slug
    qs=Product.objects.filter(slug=slug).order_by('-id')
    exists=qs.exists()
    if exists:
        new_slug='%s-%s' %  (slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_receiver,Product)


@property
def avg_rating(self):
    ratings = self.ratings.all()
    if ratings.exists():
        return round(sum(r.rating for r in ratings) / ratings.count(), 1)
    return 0
  


class Product_Image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    Image_url=models.CharField(max_length=200)



class Additional_Information(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    spacification=models.CharField(max_length=100)
    detail=models.CharField(max_length=200)


class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    amount = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=300, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True)
    date = models.DateField(auto_now_add=True)
    order_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    payment_details = models.JSONField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Placed',
    )  

    def __str__(self):
        return self.user.username

    

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.CharField(max_length=200)
    image=models.ImageField(upload_to='Product_Images/Order')
    quantity=models.CharField(max_length=200)
    price=models.CharField(max_length=50)
    total=models.CharField(max_length=1000)


    def __str__(self):
        return self.order.user.username
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    


class banner(models.Model):

    DEAL=(
    ('Bestseller Products','Bestseller Products'),
    ('Featured Products','Featured Products')
                    )


    Image=models.ImageField(upload_to='banner_img')
    Deal=models.CharField(choices=DEAL,max_length=100,null=True)
    Quote=models.CharField(max_length=100)
    Discount=models.IntegerField()
    Link=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Quote
    

class banner_Section(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ban_section(models.Model):
    sectionn=models.ForeignKey(banner_Section,on_delete=models.DO_NOTHING)
    Image=models.ImageField(upload_to='media/banner_section')
    Quote=models.CharField(max_length=100)
    Discount=models.IntegerField()
    Link=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Quote




class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # from 1 to 5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # prevent multiple ratings from same user

    def __str__(self):
        return f"{self.product.product_name} - {self.rating} Star"
