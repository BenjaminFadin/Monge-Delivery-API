from django.db import models
from shared.models import BaseModel

UZ = "uz"
RU = "ru"
EN = 'en'

class User(BaseModel):
    LANGUAGE_CHOICE = (
        (UZ, 'uz'),
        (RU, 'ru'),
        (EN, 'en')
    )

    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICE, null=True, blank=True)
    birth_date = models.DateField()
    is_courier = models.BooleanField(default=False)  

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'User'

    def __str__(self):
        user_info = f"ID: {self.telegram_id}, {self.username}"
        return user_info

x