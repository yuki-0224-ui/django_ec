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


class ProductImage(models.Model):
    class Meta:
        db_table = 'product_images'

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path, blank=True,)
    image_alt = models.CharField(max_length=100)

    def __str__(self):
        return self.product.name
