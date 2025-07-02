# pets/views.py
from rest_framework import viewsets, permissions
from .models import Pet, PetType, PetSpecies, WeightLog, HealthLog, InjectionLog
from .serializers import PetSerializer, PetTypeSerializer, PetSpeciesSerializer, WeightLogSerializer, HealthLogSerializer, InjectionLogSerializer

# 確保只有主人才能修改
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class PetViewSet(viewsets.ModelViewSet):
    # 對寵物資料的CRUD API

    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    # 權限設定
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # 只回傳當前使用者的寵物
        return self.request.user.pets.all()

    def perform_create(self, serializer):
        # 新增寵物時，自動將owner設為當前使用者
        serializer.save(owner=self.request.user)

class PetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    # 提供寵物類型列表

    queryset = PetType.objects.all()
    serializer_class = PetTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PetSpeciesViewSet(viewsets.ReadOnlyModelViewSet):
    # 提供品種列表，連動式選單

    queryset = PetSpecies.objects.all()
    serializer_class = PetSpeciesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 根據URL中的pet_type_pk過濾品種
        pet_type_pk = self.kwargs.get('pet_type_pk')
        if pet_type_pk:
            return PetSpecies.objects.filter(pet_type_id=pet_type_pk)
        return PetSpecies.objects.none() # 如果還沒選type，不提供值

# 體重日誌區
class WeightLogViewSet(viewsets.ModelViewSet):
    # 提供寵物的體重紀錄的 CRUD API

    queryset = WeightLog.objects.all()
    serializer_class = WeightLogSerializer
    permission_classes = [permissions.IsAuthenticated] # 權限：必須登入

    def get_queryset(self):
        # 回傳指定pet_pk的體重紀錄。

        # 從URL中取得pk
        pet_pk = self.kwargs.get('pet_pk')
        if pet_pk:
            # 比洞寵物主人是當前使用者
            return WeightLog.objects.filter(pet__pk=pet_pk, pet__owner=self.request.user)
        return WeightLog.objects.none()
    def perform_create(self, serializer):

        # 新增體重紀錄時，自動設定關聯
        pet_pk = self.kwargs.get('pet_pk')
        # 確保該寵物存在且屬於當前使用者
        pet = Pet.objects.get(pk=pet_pk, owner=self.request.user)
        serializer.save(pet=pet)


# 健康日誌區
class HealthLogViewSet(viewsets.ModelViewSet):
    # 提供寵物的健康日誌的 CRUD API
    # 邏輯基本上與體重區相同，多一個圖片上傳

    queryset = HealthLog.objects.all()
    serializer_class = HealthLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        pet_pk = self.kwargs.get('pet_pk')
        if pet_pk:
            return HealthLog.objects.filter(pet__pk=pet_pk, pet__owner=self.request.user)
        return HealthLog.objects.none()

    def perform_create(self, serializer):
        # 新增日誌時，自動關聯寵物並處理圖片上傳。

        pet_pk = self.kwargs.get('pet_pk')
        pet = Pet.objects.get(pk=pet_pk, owner=self.request.user)
        photo = self.request.FILES.get('photo_records')
        serializer.save(pet=pet, photo_records=photo)

# 驅蟲日誌區
class InjectionLogViewSet(viewsets.ModelViewSet):
    # 提供寵物的疫苗/驅蟲紀錄的 CRUD API

    queryset = InjectionLog.objects.all()
    serializer_class = InjectionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        pet_pk = self.kwargs.get('pet_pk')
        if pet_pk:
            return InjectionLog.objects.filter(pet__pk=pet_pk, pet__owner=self.request.user)
        return InjectionLog.objects.none()

    def perform_create(self, serializer):

        pet_pk = self.kwargs.get('pet_pk')
        pet = Pet.objects.get(pk=pet_pk, owner=self.request.user)
        serializer.save(pet=pet)