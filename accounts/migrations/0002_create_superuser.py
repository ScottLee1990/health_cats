# accounts/migrations/0002_create_superuser.py

from django.db import migrations
import os # 引入 os 來讀取環境變數

def create_superuser(apps, schema_editor):
    """
    在遷移過程中，建立一個超級使用者。
    """
    # 從 apps.get_model 取得 User 模型，這是遷移檔案中的標準做法
    User = apps.get_model('auth', 'User')

    # 從環境變數讀取超級使用者的帳號、信箱和密碼
    # 這樣可以避免將密碼等敏感資訊直接寫死在程式碼中
    # 我們稍後會在 Render 平台上設定這些環境變數
    DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME')
    DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL')
    DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')

    # 只有在三個環境變數都存在的情況下才繼續
    if DJANGO_SU_NAME and DJANGO_SU_EMAIL and DJANGO_SU_PASSWORD:
        # 檢查同名使用者是否已存在
        if not User.objects.filter(username=DJANGO_SU_NAME).exists():
            print(f'Creating superuser: {DJANGO_SU_NAME}')
            User.objects.create_superuser(
                username=DJANGO_SU_NAME,
                email=DJANGO_SU_EMAIL,
                password=DJANGO_SU_PASSWORD
            )
        else:
            print(f'Superuser {DJANGO_SU_NAME} already exists.')

class Migration(migrations.Migration):

    # 這個遷移檔案依賴於 accounts app 的初始遷移
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # 告訴 Django 在執行這次遷移時，要運行我們的 Python 函式
        migrations.RunPython(create_superuser),
    ]