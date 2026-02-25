from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,
    ClientBrandViewSet,
    DistrictViewSet,
    RegionViewSet,
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'client-brands', ClientBrandViewSet, basename='client-brands')
router.register(r'district', DistrictViewSet, basename='district')
router.register(r'region', RegionViewSet, basename='region')

urlpatterns = router.urls