import uuid
from django.db import models

from utils.models import CreateUpdateTracker, nb, GetOrNoneManager


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Название категории', max_length=256)
    image = models.ImageField('Титульная изображения', upload_to='catalog_images',
                              default='catalog_images/defoult_category.png')
    objects = GetOrNoneManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Название бренда', max_length=256)
    logo = models.ImageField('Логотип', upload_to='brand_icons')
    category = models.ManyToManyField(Category, verbose_name="Категория")
    objects = GetOrNoneManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Size(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.CharField('Размер', max_length=20)
    objects = GetOrNoneManager()

    def __str__(self):
        return self.value

    class Meta:
        ordering = ['value', ]
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Product(CreateUpdateTracker):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Название продукта', max_length=256)
    price = models.IntegerField('Цена')
    info = models.TextField('Описание')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    gender = models.CharField('Для (муж./жен./дет.):', max_length=10, default='male',
                              choices=(("male", "Мужсая"), ("female", "Женская"), ("child", "Детская")))
    size = models.ManyToManyField(Size)
    objects = GetOrNoneManager()

    def __str__(self):
        return f'{self.brand.title} - {self.title}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProdictImage(CreateUpdateTracker):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Изображение',
                                related_name='product_img')
    img = models.ImageField('Изображение', upload_to='products')

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображении'