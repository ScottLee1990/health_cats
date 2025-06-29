# pets/views.py
from rest_framework import viewsets, permissions
from .models import Pet, PetType, PetSpecies, WeightLog, HealthLog, InjectionLog
from .serializers import PetSerializer, PetTypeSerializer, PetSpeciesSerializer, WeightLogSerializer, HealthLogSerializer, InjectionLogSerializer

# IsOwner 權限：確保只有物件的主人才能修改它
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class PetViewSet(viewsets.ModelViewSet):
    """
    提供對寵物資料的 CRUD API
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    # 權限設定：必須登入，且操作時必須是主人
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # 只回傳當前登入使用者的寵物
        return self.request.user.pets.all()

    def perform_create(self, serializer):
        # 新增寵物時，自動將 owner 設為當前使用者
        serializer.save(owner=self.request.user)

class PetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    提供寵物類型的列表與詳細資料
    """
    queryset = PetType.objects.all()
    serializer_class = PetTypeSerializer
    permission_classes = [permissions.IsAuthenticated] # 登入即可讀取

class PetSpeciesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    提供寵物品種的列表，用於連動式選單
    """
    queryset = PetSpecies.objects.all()
    serializer_class = PetSpeciesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 根據 URL 中的 pet_type_pk 來過濾品種
        pet_type_pk = self.kwargs.get('pet_type_pk')
        if pet_type_pk:
            return PetSpecies.objects.filter(pet_type_id=pet_type_pk)
        return PetSpecies.objects.none() # 如果沒有提供 type，就不回傳任何東西

# 為 WeightLog 模型新增 ViewSet
class WeightLogViewSet(viewsets.ModelViewSet):
    """
    提供特定寵物的體重紀錄的 CRUD API
    """
    queryset = WeightLog.objects.all()
    serializer_class = WeightLogSerializer
    permission_classes = [permissions.IsAuthenticated] # 權限：必須登入

    def get_queryset(self):
        """
        這個 view 只應回傳 URL 中指定 pet_pk 的體重紀錄。
        """
        # 從 URL 中取得 pet 的 primary key
        pet_pk = self.kwargs.get('pet_pk')
        if pet_pk:
            # 只篩選出屬於該寵物，且該寵物的主人是當前使用者的紀錄
            return WeightLog.objects.filter(pet__pk=pet_pk, pet__owner=self.request.user)
        return WeightLog.objects.none() # 如果沒有 pet_pk，不回傳任何東西

    def perform_create(self, serializer):
        """
        新增一筆體重紀錄時，自動將其與 URL 中的 pet 關聯。
        """
        pet_pk = self.kwargs.get('pet_pk')
        # 確保該寵物存在且屬於當前使用者
        pet = Pet.objects.get(pk=pet_pk, owner=self.request.user)
        serializer.save(pet=pet)


# 為 HealthLog 模型新增 ViewSet
class HealthLogViewSet(viewsets.ModelViewSet):
    """
    提供特定寵物的健康日誌的 CRUD API
    """
    queryset = HealthLog.objects.all()
    serializer_class = HealthLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        只回傳 URL 中指定 pet_pk 的健康日誌。
        """
        pet_pk = self.kwargs.get('pet_pk')
        if pet_pk:
            return HealthLog.objects.filter(pet__pk=pet_pk, pet__owner=self.request.user)
        return HealthLog.objects.none()

    def perform_create(self, serializer):
        """
        新增日誌時，自動關聯寵物並處理圖片上傳。
        """
        pet_pk = self.kwargs.get('pet_pk')
        pet = Pet.objects.get(pk=pet_pk, owner=self.request.user)

        # 從 request.FILES 中取得上傳的圖片
        photo = self.request.FILES.get('photo_records')

        serializer.save(pet=pet, photo_records=photo)

# 為 InjectionLog 模型新增 ViewSet
class InjectionLogViewSet(viewsets.ModelViewSet):
    """
    提供特定寵物的疫苗/驅蟲紀錄的 CRUD API
    """
    queryset = InjectionLog.objects.all()
    serializer_class = InjectionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        只回傳 URL 中指定 pet_pk 的紀錄。
        """
        pet_pk = self.kwargs.get('pet_pk')
        if pet_pk:
            return InjectionLog.objects.filter(pet__pk=pet_pk, pet__owner=self.request.user)
        return InjectionLog.objects.none()

    def perform_create(self, serializer):
        """
        新增紀錄時，自動關聯寵物。
        """
        pet_pk = self.kwargs.get('pet_pk')
        pet = Pet.objects.get(pk=pet_pk, owner=self.request.user)
        serializer.save(pet=pet)