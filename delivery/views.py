from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from .models import *
from users.models import User
from rest_framework import status
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    PromotionSerializer, 
    OrderSerializer, 
    OrderItemSerializer,
    CartSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CartItemSerializer
)

class CategoryParentViewSet(ModelViewSet):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer

class SubCategoryViewSet(ModelViewSet):
    # queryset = Category.objects.filter(parent__isnull=False)
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        parent_id = self.request.query_params.get('parent_id')
        if parent_id is not None:
            return Category.objects.filter(parent_id=parent_id)
        else:
            return Category.objects.filter(parent__isnull=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    # def get_queryset(self):
    #     parent_id = self.request.query_params.get('parent_id')
    #     if parent_id:
    #         return Category.objects.filter(parent__id=parent_id)
    #     return Category.objects.none()  # Return an empty queryset if no parent_id is provided

    # @action(detail=False, methods=['get'])
    # def list_subcategories(self, request, *args, **kwargs):
    #     parent_id = request.query_params.get('parent_id')
    #     if not parent_id:
    #         return Response({"detail": "parent_id query parameter is required."}, status=400)
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # lookup_field = 'customer__id'


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data.pop('telegram_id')
        user = User.objects.get(telegram_id=telegram_id)
        cart = Cart.get_cart_for_user(user=user)
        return Response(self.serializer_class(cart).data)


class CartItemViewSet(ModelViewSet):    
    http_method_names = ['get', 'post', 'patch', 'delete']  # katta harf bilan yozsa ishlamaydi

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs.get('cart_pk')) \
            .select_related('product')


