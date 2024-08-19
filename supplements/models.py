from django.db import models
from django.utils.text import slugify


# MainCategory Model
class MainCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Main Categories'

    def __str__(self):
        return self.name


# Category Model
class Category(models.Model):
    # objects = None
    name = models.CharField(max_length=255)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name="categories")
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, editable=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save first to ensure we have an ID
        if not self.id:
            super().save(*args, **kwargs)

        # Generate the slug based on the main category name and this category's ID
        if not self.slug:
            self.slug = slugify(f"{self.main_category.name}-{self.id}")
            super().save(*args, **kwargs)  # Save again with the generated slug


# SubCategory Model
class SubCategory(models.Model):
    # objects = None
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, editable=False)

    class Meta:
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save first to ensure we have an ID
        if not self.id:
            super().save(*args, **kwargs)

        # Generate the slug based on the category name and this subcategory's ID
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.id}")
            super().save(*args, **kwargs)  # Save again with the generated slug


# Supplement Model
class Supplement(models.Model):
    name = models.CharField(max_length=255)
    main_category = models.ForeignKey(
        'MainCategory', on_delete=models.CASCADE, related_name='supplements', null=True, blank=True
    )
    categories = models.ManyToManyField(Category, related_name='supplements', blank=True)
    subcategories = models.ManyToManyField(
        'SubCategory', related_name='supplements', blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    strength = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    pictures = models.ImageField(upload_to='supplements/', null=True, blank=True)

    def __str__(self):
        return self.name


# HealthBenefit Model
class HealthBenefit(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE, related_name='benefits')
    benefit = models.CharField(max_length=255)
    dosage_form = models.CharField(max_length=255)
    clinical_study = models.FileField(upload_to='clinical_studies/')
    summary = models.FileField(upload_to='summaries/')

    def __str__(self):
        return self.benefit
