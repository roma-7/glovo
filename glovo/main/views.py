from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import *
from .permissions import *


class UserProfileListApiView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # каждыый user будет смотреть свой профиль
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    # каждыый user будет смотреть свой профиль
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class StoreListApiView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [CheckUserCreate]

    def get_queryset(self):
        return Store.objects.filter(id=self.request.user.id)



class StoreCreateApiView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [CheckUserCreate]

class StoreEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckUserCreate]

    # только owner сможет изменить
    # def get_queryset(self):
    #     return Store.objects.filter(owner=self.request.user)


class StoreDetailView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer


class ContactInfoListView(generics.ListAPIView):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('price')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductListFilter


class ProductDetailApiView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('price')
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductListFilter


class ProductCreateApiView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CheckUserCreate]


class ProductEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductComboViewSet(viewsets.ModelViewSet):
    queryset = ProductCombo.objects.all().order_by('price')
    serializer_class = ProductComboSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductComboListFilter


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)




    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class StoreReviewCreateApiView(generics.CreateAPIView):
    queryset = ReviewStore.objects.all()
    serializer_class = StoreReviewCreateSerializer
    permission_classes = [CheckReviewUser, CheckReviewEdit]

    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class StoreReviewListApiView(generics.ListAPIView):
    queryset = ReviewStore.objects.all()
    serializer_class = StoreReviewSerializer


class ProductReviewCreateApiView(generics.CreateAPIView):
    queryset = ReviewProduct.objects.all()
    serializer_class = ProductReviewCreateSerializer
    permission_classes = [CheckReviewUser, CheckReviewEdit]

    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class ProductReviewListApiView(generics.ListAPIView):
    queryset = ReviewProduct.objects.all()
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class CourierReviewCreateApiView(generics.CreateAPIView):
    queryset = ReviewCourier.objects.all()
    serializer_class = CourierReviewCreateSerializer
    permission_classes = [CheckReviewUser, CheckReviewEdit]

    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class CourierReviewListApiView(generics.ListAPIView):
    queryset = ReviewCourier.objects.all()
    serializer_class = CourierReviewSerializer


class OrderCreateApiView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class OrderListApiView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [CheckReviewUser]

    def get_queryset(self):
        return Order.objects.filter(client_order=self.request.user)


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
