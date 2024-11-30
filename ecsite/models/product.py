from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    DEFAULT_IMAGE_SRC = 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg'
    DEFAULT_IMAGE_ALT = '商品画像なし'
    DEFAULT_THUMBNAIL_SRC = 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg'
    DEFAULT_THUMBNAIL_ALT = 'サムネイル画像なし'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ecsite:product_detail', kwargs={'slug': self.slug})

    def is_sold_out(self):
        return self.stock == 0

    def _get_image_attribute(self, attribute, default):
        if self.images.exists():
            obj = self.images.all()[0]
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
    image = models.ImageField(upload_to=product_image_path, blank=True,)
    image_alt = models.CharField(max_length=100)

    def __str__(self):
        return self.product.name
