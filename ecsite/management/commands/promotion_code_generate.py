from django.core.management.base import BaseCommand
from ecsite.models.promotion import PromotionCode


class Command(BaseCommand):

    def handle(self, *args, **options):
        codes = PromotionCode.generate_codes()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully generated {len(codes)} promotion codes'))
        for code in codes:
            self.stdout.write(f'Code: {code.code}, Discount: ¥{
                              code.discount_amount}')
