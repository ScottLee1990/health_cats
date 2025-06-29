# pets/admin.py

from django.contrib import admin
from .models import Pet, PetType, PetSpecies, WeightLog, HealthLog, InjectionLog

# 將你的模型註冊到 admin 後台
admin.site.register(PetType)
admin.site.register(PetSpecies)
admin.site.register(Pet)
admin.site.register(WeightLog)
admin.site.register(HealthLog)
admin.site.register(InjectionLog)