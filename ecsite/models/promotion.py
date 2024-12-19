from django.db import models
import random
import string


class PromotionCode(models.Model):
    class Meta:
        db_table = 'promotion_codes'

    code = models.CharField(max_length=7, unique=True)
    discount_amount = models.PositiveIntegerField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_code(cls):
        while True:
            chars = string.ascii_uppercase + string.digits
            code = ''.join(random.choice(chars) for _ in range(7))
            if not cls.objects.filter(code=code).exists():
                return code

    @classmethod
    def generate_codes(cls, count=10):
        codes = []
        for _ in range(count):
            code = cls.generate_code()
            discount_amount = random.randint(100, 1000)
            codes.append(cls(code=code, discount_amount=discount_amount))
        return cls.objects.bulk_create(codes)
