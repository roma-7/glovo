from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'product-combos', ProductComboViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'couriers', CourierViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('', include(router.urls)),
    path('users/', UserProfileListApiView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailListView.as_view(), name='user_detail'),
    path('store/', StoreListApiView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailView.as_view(), name='store_detail'),
    path('store/create/', StoreCreateApiView.as_view(), name='store_create'),
    path('store/create/<int:pk>', StoreEditApiView.as_view(), name='store_edit'),
    path('products/', ProductListApiView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailApiView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateApiView.as_view(), name='product_create'),
    path('products/create/<int:pk>', ProductEditApiView.as_view(), name='product_edit'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('contact_info/', ContactInfoListView.as_view(), name='contact_info_list'),
    path('contact_info/<int:pk>/', ContactInfoListView.as_view(), name='contact_info_detail'),
    path('orders/', OrderListApiView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateApiView.as_view(), name='order_create'),
    path('store/<int:pk>/edit/', StoreEditApiView.as_view(), name='store_edit'),
    path('products/<int:pk>/edit/', ProductEditApiView.as_view(), name='product_edit'),
    path('reviews/store/create/', StoreReviewCreateApiView.as_view(), name='store_review_create'),
    path('reviews/store/', StoreReviewListApiView.as_view(), name='store_review_list'),
    path('reviews/product/create/', ProductReviewCreateApiView.as_view(), name='product_review_create'),
    path('reviews/product/', ProductReviewListApiView.as_view(), name='product_review_list'),
    path('reviews/courier/create/', CourierReviewCreateApiView.as_view(), name='courier_review_create'),
    path('reviews/courier/', CourierReviewListApiView.as_view(), name='courier_review_list'),
]
