# pets/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # 使用有時區意識的時間
from datetime import timedelta

# 使用 Django 4.0+ 的 TextChoices 讓選項更清晰
class PetGender(models.TextChoices):
    MALE = 'M', '公'
    FEMALE = 'F', '母'
    UNKNOWN = 'UNK', '未知'

class HealthAction(models.TextChoices):
    SEE_DOCTOR = 'SEE_DOCTOR', '就醫'
    OBSERVATION = 'OBSERVATE', '觀察'
    NORMAL = 'NORMAL', '正常'

class FoodBrandChoices(models.TextChoices):
    ROYAL_CANIN = 'RC', '皇家'
    HILLS = 'HILLS', '希爾思'
    ORIJEN = 'ORIJEN', '渴望'
    NUTRAM = 'NUTRAM', '紐頓'
    CATPOOL = 'CATPOOL', '貓侍'
    NUTRIENCE = 'NUTRIENCE', '紐崔斯'


# --- Pet 分類模型 ---
class PetType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 例如: 貓, 狗, 鼠
    def __str__(self):
        return self.name

class PetSpecies(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 例如: 米克斯, 哈士奇
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name='species')

    def __str__(self):
        return self.name

# --- 主要模型 ---
class Pet(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    pet_type = models.ForeignKey(PetType, on_delete=models.SET_NULL, null=True, related_name='pets_of_type')
    pet_species = models.ForeignKey(PetSpecies, on_delete=models.SET_NULL, null=True, related_name='pets_of_species')
    gender = models.CharField(max_length=3, choices=PetGender.choices, default=PetGender.MALE)

    photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    birth_day = models.DateField()
    favorite_food = models.CharField(max_length=10, choices=FoodBrandChoices.choices, blank=True)
    memo = models.TextField(blank=True, verbose_name="備註")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        # 更精確的年齡計算方式
        today = timezone.now().date()
        # 計算年份差異，並檢查生日是否已過
        return today.year - self.birth_day.year - (
                    (today.month, today.day) < (self.birth_day.month, self.birth_day.day))

    def __str__(self):
        # __str__ 必須回傳一個字串 (string)
        return f"{self.name} ({self.owner.username})"


class InjectionLog(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='injection_logs')
    injection_type = models.CharField(max_length=100)  # 例如: '狂犬病疫苗' or '三合一'
    note = models.TextField(blank=True)
    injection_date = models.DateField(default=timezone.now, verbose_name="施打日期")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.injection_type}"

    @property
    def next_date(self):
        # 【修改】計算下次日期時，應基於施打日期而不是建立日期
        if self.injection_date:
            return self.injection_date + timedelta(days=30) # 假設一年一次
        return None


class HealthLog(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='health_logs')
    topic = models.CharField(max_length=200)
    content = models.TextField()
    photo_records = models.ImageField(upload_to='health_log_photos/', blank=True, null=True)
    action = models.CharField(max_length=20, choices=HealthAction.choices)
    case_closed = models.BooleanField(default=False, verbose_name="是否結案")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # __str__ 必須回傳一個字串
        return f"{self.topic} ({self.get_action_display()})"

class WeightLog(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='weight_logs')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2) # 使用 DecimalField 更精確
    recorded_at = models.DateField(default=timezone.now) # 記錄日期

    class Meta:
        # 讓最近的紀錄排在最前面
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.pet.name} - {self.weight_kg}kg on {self.recorded_at}"
