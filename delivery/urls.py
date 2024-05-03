from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
# router.register('category-parent', views.CategoryParentViewSet, basename='category_parent')
# router.register('category-child', views.CategoryParentViewSet, basename='category_child')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('order-items', views.OrderItemViewSet, basename='order-items')
router.register('carts', views.CartViewSet, basename='carts')


# URL conf
urlpatterns = router.urls
