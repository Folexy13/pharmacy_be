from django.contrib import admin

from .form import SupplementForm
from .models import MainCategory, Category, SubCategory, Supplement, HealthBenefit


# Register your models here.

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_category', 'description','slug')
    readonly_fields = ('slug',)  # Make 'slug' field read-only in the admin


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description','slug')
    readonly_fields = ('slug',)  # Make 'slug' field read-only in the admin


class HealthBenefitInline(admin.TabularInline):
    model = HealthBenefit


@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    form = SupplementForm
    list_display = ('name', 'price', 'strength', 'description', 'get_categories', 'get_subcategories')

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

    def get_subcategories(self, obj):
        # Create a dictionary to group subcategories by their parent category
        grouped_subcategories = {}
        
        for subcategory in obj.subcategories.all():
            parent_category = subcategory.category
            if parent_category not in grouped_subcategories:
                grouped_subcategories[parent_category] = []
            grouped_subcategories[parent_category].append(subcategory)
        
        # Format the dictionary into a readable string
        formatted_subcategories = []
        for parent_category, subcategories in grouped_subcategories.items():
            subcat_names = ", ".join([subcat.name for subcat in subcategories])
            formatted_subcategories.append(f"{parent_category.name}: {subcat_names}")
        
        return "; ".join(formatted_subcategories)
    get_subcategories.short_description = 'Subcategories'
    
    inlines = [HealthBenefitInline]

    class Media:
        js = ('/static/supplement_admin.js',)

