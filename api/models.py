from django.db import models
from .validators import validate_phone_number
from django.core.validators import MinValueValidator

# Create your models here.


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transation(AbstractBaseModel):
    phone_number = models.CharField(max_length=15)
    amount = models.PositiveIntegerField(validators=[MinValueValidator])
    receipt_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.receipt_no


class ResponseBody(AbstractBaseModel):
    body = models.JSONField()

    class Meta:
        get_latest_by = "created_at"

    def __str__(self):
        return self.created_at
