from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


def product_image_path(instance, filename):
    return f'ecsite/{instance.product.slug}/{filename}'


class Product(models.Model):
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    DEFAULT_IMAGE_SRC = 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg'
    DEFAULT_IMAGE_ALT = '商品画像なし'
    DEFAULT_THUMBNAIL_SRC = 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg'
    DEFAULT_THUMBNAIL_ALT = 'サムネイル画像なし'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self._should_update_slug():
            self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _should_update_slug(self):
        if not self.pk:
            return False
        existing_product = Product.objects.get(pk=self.pk)
        return existing_product.name != self.name

    def _generate_unique_slug(self):
        slug = slugify(self.name)
        self.slug = slug

    def get_absolute_url(self):
        return reverse('ecsite:product_detail', kwargs={'slug': self.slug})

    def is_sold_out(self):
        return self.stock == 0

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    # def restore(self):
    #     self.is_deleted = False
    #     self.deleted_at = None
    #     self.save()

    @classmethod
    def get_available(cls):
        return cls.objects.filter(is_deleted=False)

    def _get_image_attribute(self, attribute, default):
        if self.images.exists():
            obj = self.images.all()[0]
            if attribute.startswith('image.') and not obj.image:
                return default
            for attr in attribute.split('.'):
                obj = getattr(obj, attr, default)
                if obj == default:
                    break
            return obj
        return default

    def get_main_image_url(self):
        return self._get_image_attribute('image.url', self.DEFAULT_IMAGE_SRC)

    def get_main_image_alt(self):
        return self._get_image_attribute('image_alt', self.DEFAULT_IMAGE_ALT)

    def get_thumbnail_url(self):
        return self._get_image_attribute('image.url', self.DEFAULT_THUMBNAIL_SRC)

    def get_thumbnail_alt(self):
        return self._get_image_attribute('image_alt', self.DEFAULT_THUMBNAIL_ALT)


class ProductImage(models.Model):
    class Meta:
        db_table = 'product_images'

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path, blank=True)
    image_alt = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.product.name
