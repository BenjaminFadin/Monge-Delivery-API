from rest_framework_nested import routers

from users import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet, basename='users')


# URL conf
urlpatterns = router.urls

