from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="catalog/image", verbose_name="Изображение", blank=True, null=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateField(blank=True, null=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        blank=True, null=True, verbose_name="Дата последнего изменения"
    )
    active_version = models.ForeignKey(
        "Version",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_products",
        verbose_name="Активная версия"
    )
    views_counter = models.PositiveIntegerField(
        default=0,
        verbose_name="Счётчик просмотров",
        help_text="Укажите количество просмотров",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )
    content = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="catalog/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите фото продукта",
    )
    date_creation = models.DateField(
        verbose_name="Дата создания", blank=True, null=True
    )
    publication_sign = models.BooleanField(
        verbose_name="Уже опубликовано?", default=False
    )
    views_counter = models.PositiveIntegerField(
        default=0,
        verbose_name="Счётчик просмотров",
        help_text="Укажите количество просмотров",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:blog_detail", kwargs={"pk": self.pk, "slug": self.slug})

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["publication_sign", "-date_creation"]


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="versions",
        null=True,
        blank=True,
        verbose_name="Продукт",
    )
    version_number = models.PositiveIntegerField(
        verbose_name="Номер версии",
        help_text="Введите номер версии",
    )
    version_name = models.CharField(
        verbose_name="Название версии",
        help_text="Введите название версии",
        blank=True,
        null=True,
    )
    indication_current_version = models.BooleanField(
        verbose_name="Признак текущей версии.",
        help_text="Введите признак текущей версии",
        default=False,
    )

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продуктов"
        ordering = ["indication_current_version", "version_number"]
