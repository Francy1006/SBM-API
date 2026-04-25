from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ModuleViewSet,
    ModuleOrderConfigViewSet,
    ModuleOrderCalculationDetailViewSet,
    VariableFormulaViewSet,
    ModuleOrderFormulaView,
    ModuleOrderFormulaDetailView,
    ModuleOrderVariablesView,  # <-- FIX (antes: ModuleOrderVariableView)
)

router = DefaultRouter()
router.register(r"module", ModuleViewSet)
router.register(r"module-order-configs", ModuleOrderConfigViewSet)
router.register(
    r"module-order-calculation-details",
    ModuleOrderCalculationDetailViewSet,
    basename="module-order-calculation-detail",
)
router.register(r"variable-formulas", VariableFormulaViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("module-order-formula/", ModuleOrderFormulaView.as_view()),
    path("module-order-formula-detail/", ModuleOrderFormulaDetailView.as_view()),
    path("module-order-variables/", ModuleOrderVariablesView.as_view()),
]