from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .filters import *
from .permissions import *
from .pagination import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.views import LogoutView
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


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
    pagination_class = LargeResultsSetPagination


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    pagination_class = StandardResultsSetPagination


class StoreListApiView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = LargeResultsSetPagination


class StoreCreateApiView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [CheckUserCreate]


class StoreEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckUserCreate]


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
    pagination_class = LargeResultsSetPagination


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all().order_by('price')
    serializer_class = ProductDetailSerializer
    pagination_class = StandardResultsSetPagination


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
    pagination_class = LargeResultsSetPagination

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
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Order.objects.filter(client_order=self.request.user)


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
