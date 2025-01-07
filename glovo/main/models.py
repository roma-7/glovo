from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    ROLE_CHOICES = (
        ('owner', 'owner'),
        ('client', 'client'),
        ('courier', 'courier'),
    )

    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='client')
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} -- {self.role}'


class Store(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=32, unique=True, )
    store_image = models.ImageField(upload_to='store_images/')
    description = models.TextField()
    address = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.store_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f'{self.category_name}'


class ContactInfo(models.Model):
    contact_info = PhoneNumberField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contact_info} -- {self.store}'


class Product(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=64)
    product_image = models.ImageField(upload_to='product_images/')
    price = models.PositiveSmallIntegerField()
    description = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')

    def __str__(self):
        return f'{self.product_name} -- {self.store}'


class ProductCombo(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    combo_name = models.CharField(max_length=64)
    combo_image = models.ImageField(upload_to='product_images/')
    price = models.PositiveSmallIntegerField()
    description = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_combo_category')

    def __str__(self):
        return f'{self.combo_name} -- {self.store}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.cart}, -- {self.product}, {self.quantity}'


class Courier(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='couriers')
    STATUS_COURIER_CHOICES = (
        ('доступен', 'доступен'),
        ('занят', 'занят')
    )
    status = models.CharField(max_length=10, choices=STATUS_COURIER_CHOICES, default='доступен')
    current_orders = models.ForeignKey(Product, related_name='couriers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.status}'


class Order(models.Model):
    product_order = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    STATUS_ORDER_CHOICES = (
        ('ожидает', 'ожидает'),
        ('в процессе', 'в процессе'),
        ('доставлен', 'доставлен'),
        ('отменен', 'отменен'),
    )
    status_order = models.CharField(max_length=32, choices=STATUS_ORDER_CHOICES, default='ожидает')
    client_order = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client_order}, - {self.product_order} - {self.status_order}'


class ReviewStore(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_reviews', null=True, blank=True)
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='рейтинг', null=True,
                                blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_name}, - {self.stars}'


class ReviewProduct(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews', null=True,
                                blank=True)
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='рейтинг', null=True,
                                blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_name}, - {self.stars}'


class ReviewCourier(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='courier_reviews', null=True,
                                blank=True)
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='рейтинг', null=True,
                                blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_name}, - {self.stars}'
