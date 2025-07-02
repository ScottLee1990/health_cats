# pets/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import PetViewSet, PetTypeViewSet, PetSpeciesViewSet, WeightLogViewSet, HealthLogViewSet, InjectionLogViewSet

router = routers.DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'pet-types', PetTypeViewSet, basename='pet-type')

# Nested Router -> 處理連動選單
# 產生 URL: /pet-types/{pet_type_pk}/species/
pet_types_router = routers.NestedSimpleRouter(router, r'pet-types', lookup='pet_type')
pet_types_router.register(r'species', PetSpeciesViewSet, basename='pet-type-species')

# 這會產生 URL: /api/pets/{pet_pk}/weight-logs/
pets_router = routers.NestedSimpleRouter(router, r'pets', lookup='pet')
pets_router.register(r'weight-logs', WeightLogViewSet, basename='pet-weight-logs')
pets_router.register(r'health-logs', HealthLogViewSet, basename='pet-health-logs')
pets_router.register(r'injection-logs', InjectionLogViewSet, basename='pet-injection-logs')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(pet_types_router.urls)),
    path('', include(pets_router.urls)),
]
