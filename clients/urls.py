from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ClientBrandViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'client-brands', ClientBrandViewSet, basename='client-brands')

urlpatterns = router.urls