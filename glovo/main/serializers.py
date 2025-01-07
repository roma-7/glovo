from .models import *
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', ]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'date_registered']


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id', 'contact_info', 'store']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_image', 'price', 'description', ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_image', 'price', 'description']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'store_name', 'store_image']


class StoreDetailSerializer(serializers.ModelSerializer):
    store_product = ProductListSerializer(many=True, read_only=True)
    contact_info = ContactInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'address', 'description', 'store_product', 'contact_info']


class ProductComboSerializer(serializers.ModelSerializer):
    store = StoreListSerializer(read_only=True)

    class Meta:
        model = ProductCombo
        fields = ['id', 'combo_name', 'combo_image', 'price', 'description', 'store', ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    product_category = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'product_category']


class CartSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_date']


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price


class OrderSerializer(serializers.ModelSerializer):
    client_order = UserProfileSerializer(read_only=True)
    product_order = CartItemSerializer(read_only=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['product_order', 'delivery_address', 'status_order', 'client_order', 'cart']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product_order', 'delivery_address', 'client_order', 'cart']


class CourierSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    current_orders = ProductListSerializer(read_only=True)

    class Meta:
        model = Courier
        fields = ['id', 'user', 'status', 'current_orders']


class StoreReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStore
        fields = '__all__'


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewProduct
        fields = '__all__'


class CourierReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCourier
        fields = '__all__'


class StoreReviewSerializer(serializers.ModelSerializer):
    user_name = UserProfileSerializer(read_only=True)
    store = StoreListSerializer(read_only=True)

    class Meta:
        model = ReviewStore
        fields = ['id', 'user_name', 'store', 'text', 'stars', 'parent']


class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = UserProfileSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = ReviewProduct
        fields = ['id', 'user_name', 'product', 'text', 'stars', 'parent']


class CourierReviewSerializer(serializers.ModelSerializer):
    user_name = UserProfileSerializer(read_only=True)
    courier = CourierSerializer(read_only=True)

    class Meta:
        model = ReviewCourier
        fields = ['id', 'user_name', 'courier', 'text', 'stars', 'parent']
