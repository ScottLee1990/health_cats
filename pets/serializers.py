# pets/serializers.py
from rest_framework import serializers
from .models import Pet, PetType, PetSpecies, WeightLog, HealthLog, InjectionLog


class PetSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSpecies
        fields = ['id', 'name']

class PetTypeSerializer(serializers.ModelSerializer):
    # 使用上面的 PetSpeciesSerializer 來巢狀顯示所有品種
    species = PetSpeciesSerializer(many=True, read_only=True)

    class Meta:
        model = PetType
        fields = ['id', 'name', 'species']

class WeightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLog
        fields = ['id', 'weight_kg', 'recorded_at']

class PetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    pet_type = serializers.CharField(source='pet_type.name', read_only=True)
    pet_species = serializers.CharField(source='pet_species.name', read_only=True)
    favorite_food_display = serializers.CharField(source='get_favorite_food_display', read_only=True)

    pet_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PetType.objects.all(), source='pet_type', write_only=True
    )
    pet_species_id = serializers.PrimaryKeyRelatedField(
        queryset=PetSpecies.objects.all(), source='pet_species', write_only=True
    )

    # 給前端的各項計算參數
    tracking_log_count = serializers.SerializerMethodField()
    next_injection_date = serializers.SerializerMethodField()
    last_weight = serializers.SerializerMethodField()
    sterilised_display = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'owner', 'age',
            'pet_type', 'pet_species', 'gender', 'birth_day',
            'photo', 'created_at', 'updated_at', 'memo', 'favorite_food', 'favorite_food_display',
            'pet_type_id', 'pet_species_id',
            'tracking_log_count',  # 將新欄位加入 fields 中
            'next_injection_date',
            'last_weight',
            'sterilised',
            'sterilised_display',
        ]

    # *** 新增這個函式，用來計算 tracking_log_count 的值 ***
    def get_tracking_log_count(self, obj):
        # 計算這隻寵物 (obj) 有多少筆 health_logs 的 case_closed 是 False
        return obj.health_logs.filter(case_closed=False).count()

    # *** 新增這個函式，用來計算 next_injection_date 的值 ***
    def get_next_injection_date(self, obj):
        # 找到這隻寵物最近的一筆疫苗紀錄
        latest_injection = obj.injection_logs.order_by('-injection_date').first()
        if latest_injection and latest_injection.next_date:
            return latest_injection.next_date.strftime('%Y-%m-%d')
        return None

    def get_last_weight(self, obj):
        latest = obj.weight_logs.order_by('-recorded_at').first()
        if latest:
            return {
                'weight_kg': float(latest.weight_kg),
                'recorded_at': latest.recorded_at.strftime('%Y-%m-%d')
            }
        return None

    def get_sterilised_display(self, obj):
        return "已絕育" if obj.sterilised else "未絕育"


# 為 HealthLog 模型新增 Serializer
class HealthLogSerializer(serializers.ModelSerializer):
    # 讓 action 欄位在讀取時顯示可讀的名稱 (例如 '就醫') 而不是 'SEE_DOCTOR'
    action = serializers.CharField(source='get_action_display', read_only=True)
    # 讓前端寫入時可以傳 'SEE_DOCTOR'
    action_write = serializers.CharField(write_only=True, source='action')

    class Meta:
        model = HealthLog
        # photo_records 是唯讀的，因為我們會從請求的 files 中取得
        fields = ['id', 'topic', 'content', 'photo_records', 'action', 'action_write', 'case_closed', 'created_at', ]
        read_only_fields = ['photo_records']

# 為 InjectionLog 模型新增 Serializer
class InjectionLogSerializer(serializers.ModelSerializer):
    # 使用 ReadOnlyField 來序列化模型中的 property 方法
    next_date = serializers.ReadOnlyField()

    class Meta:
        model = InjectionLog
        fields = ['id', 'injection_type', 'note', 'injection_date', 'created_at', 'next_date']
        read_only_fields = ['created_at']