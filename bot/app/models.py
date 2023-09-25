from django.db import models


class Client(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    client_status = models.CharField(max_length=20, blank=True, null=True)
    preferences = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.full_name or f"User ID: {self.user_id}"


class EquipmentCategory(models.Model):
    title = models.CharField(max_length=50)
    button_text = models.CharField(max_length=150, default='')

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class EquipmentCatalog(models.Model):
    card = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    price_below_600k = models.BooleanField(default=False)
    price_below_1_5m = models.BooleanField(default=False)
    price_below_3m = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='eq_catalog/')

    class Meta:
        verbose_name_plural = 'Каталоги'

    def __str__(self):
        return self.title


class GeneralCatalog(models.Model):
    pdf_file = models.FileField(upload_to='general_catalog/', verbose_name='PDF файл Общего каталога')

    class Meta:
        verbose_name = 'Общий каталог'
        verbose_name_plural = 'Общие каталоги'

    def __str__(self):
        return 'Общий каталог'
