from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VariableFormulaViewSet, CalculationConceptViewSet, VariableFormulaView

router = DefaultRouter()
router.register(r"variable-formulas", VariableFormulaViewSet)
router.register(r"calculation-concepts", CalculationConceptViewSet)

urlpatterns = [
    path("formula-variables/", VariableFormulaView.as_view(), name="formula-variables"),
    path("", include(router.urls)),
]
