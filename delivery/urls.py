from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('categories-parent', views.CategoryParentViewSet, basename='categories-parentt')
router.register('categories-sub', views.SubCategoryViewSet, basename='categories-sub')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('order-items', views.OrderItemViewSet, basename='order-items')
router.register('carts', views.CartViewSet, basename='carts')


carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items-detail')

# URL conf
urlpatterns = router.urls + carts_router.urls
